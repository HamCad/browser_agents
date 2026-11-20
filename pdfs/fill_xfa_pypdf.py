#!/usr/bin/env python3
"""DAF 1206 XFA filler - true incremental update. Needs pypdf + (cryptography or pycryptodome).

Changes ONLY the XFA 'datasets' stream. The original file bytes are kept verbatim; one
re-encrypted object and a new xref section are appended (the same way Adobe Reader saves
a filled form). Preserved: every XFA packet incl. 'form', /Perms (usage rights), the
original encryption dictionary/key/permissions, and all other structure.

usage: python fill_daf1206_incremental.py blank.pdf filled.pdf
"""
import sys, re, os, zlib, struct, hashlib
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
from pypdf import PdfReader
from pypdf._crypt_providers import aes_cbc_encrypt

DATA = {
  "award": "Sample Civilian of the Year (SYNTHETIC)",
  "category": "Civilian",
  "awardPeriod": "1 Jan 2025 - 31 Dec 2025",
  "rankName": "Ms. Jane Q. Testperson",
  "majcom_foa_dru": "ACC / Test Wing (FAKE)",
  "DAFSC": "GS-12 / Program Analyst",
  "nomineeTelephone": "DSN 555-0142 / Comm (555) 010-0142",
  "officeAddress": "999 CS/SCO, 123 Example Blvd, Fakebase AFB, ST 00000",
  "rank": "Lt Col John A. Sample / DSN 555-0100 / Comm (555) 010-0100",
  "specificAccomplishments": "- Synthetic bullet one\n- Synthetic bullet two\n- Synthetic bullet three",
  "p2Name": "Ms. Jane Q. Testperson",
  "p2SpecificAccomplishments": "- Synthetic continuation bullet one\n- Synthetic continuation bullet two",
}

src, dst = sys.argv[1], sys.argv[2]
orig = open(src, "rb").read()
r = PdfReader(src)
encrypted = r.is_encrypted
if encrypted:
    r.decrypt("")
tr = r.trailer

# 1. locate datasets stream and build new XML
xfa = tr["/Root"]["/AcroForm"]["/XFA"]
ref = next(xfa[i + 1] for i in range(0, len(xfa), 2) if str(xfa[i]) == "datasets")
num, gen = ref.idnum, ref.generation
xml = ref.get_object().get_data().decode("utf-8")
for k, v in DATA.items():
    pat = re.compile(r"<%s\s*/>|<%s\s*>.*?</%s\s*>" % ((re.escape(k),) * 3), re.S)
    if not pat.search(xml):
        print("WARNING: field not in datasets:", k); continue
    xml = pat.sub(lambda m: f"<{k}>{escape(v)}</{k}>", xml, count=1)
ET.fromstring(xml)                                       # still valid XML
if xml == ref.get_object().get_data().decode("utf-8"):    # nothing to change -> exact copy
    open(dst, "wb").write(orig)
    print("no field values changed; wrote byte-identical copy")
    sys.exit(0)

# 2. compress, then encrypt with the file's own key (AESV2 per-object key, PDF spec 7.6.2)
body = zlib.compress(xml.encode("utf-8"))
if encrypted:
    enc = r._encryption
    ed = tr["/Encrypt"]
    if int(ed["/V"]) != 4 or str(ed["/CF"][str(ed["/StmF"])]["/CFM"]) != "/AESV2":
        sys.exit("unsupported crypt filter (script handles AESV2 / R4)")
    k = hashlib.md5(enc._key + struct.pack("<I", num)[:3] + struct.pack("<I", gen)[:2] + b"sAlT").digest()[:16]
    pad = 16 - len(body) % 16
    iv = os.urandom(16)
    body = iv + aes_cbc_encrypt(k, iv, body + bytes([pad]) * pad)

# 3. append object + xref stream (xref streams are never encrypted)
out = bytearray(orig)
if not out.endswith(b"\n"):
    out += b"\n"
obj_off = len(out)
out += b"%d %d obj\n<</Filter/FlateDecode/Length %d>>stream\n" % (num, gen, len(body)) + body + b"\nendstream\nendobj\n"

prev = int(re.findall(rb"startxref\s+(\d+)", orig)[-1])
size = max(int(tr["/Size"]), num + 1)
xref_num = size; size += 1
xref_off = len(out)
rows = [(num, struct.pack(">BIH", 1, obj_off, gen)), (xref_num, struct.pack(">BIH", 1, xref_off, 0))]
rows.sort()
index = b" ".join(b"%d 1" % n for n, _ in rows)
xdata = zlib.compress(b"".join(row for _, row in rows))
root = tr.raw_get("/Root"); info = tr.raw_get("/Info") if "/Info" in tr else None
encref = tr.raw_get("/Encrypt") if encrypted else None
ids = tr["/ID"]
idhex = b"[<%s><%s>]" % (ids[0].original_bytes.hex().encode(), ids[1].original_bytes.hex().encode())
d = b"<</Type/XRef/Size %d/Index[%s]/W[1 4 2]/Root %d %d R" % (size, index, root.idnum, root.generation)
if info is not None: d += b"/Info %d %d R" % (info.idnum, info.generation)
if encref is not None: d += b"/Encrypt %d %d R" % (encref.idnum, encref.generation)
d += b"/ID%s/Prev %d/Filter/FlateDecode/Length %d>>" % (idhex, prev, len(xdata))
out += b"%d 0 obj\n" % xref_num + d + b"stream\n" + xdata + b"\nendstream\nendobj\nstartxref\n%d\n%%%%EOF\n" % xref_off
open(dst, "wb").write(out)

# 4. verify
r2 = PdfReader(dst)
if r2.is_encrypted: r2.decrypt("")
x = r2.trailer["/Root"]["/AcroForm"]["/XFA"]
pk = {str(x[i]): x[i + 1].get_object().get_data() for i in range(0, len(x), 2)}
f = ET.fromstring(pk["datasets"]).find(".//form1")
print("original bytes preserved:", bytes(out[:len(orig)]) == orig)
print("still encrypted:", PdfReader(dst).is_encrypted, "| /Perms kept:", "/Perms" in r2.trailer["/Root"])
print("packets:", list(pk))
print("filled:", sum(bool((c.text or "").strip()) for c in f), "/", len(f))
