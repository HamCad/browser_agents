#!/usr/bin/env python3
"""Standalone DAF 1206 XFA filler. Needs only pypdf (+ cryptography or pycryptodome for AES).
usage: python fill_daf1206.py blank.pdf filled.pdf"""
import sys, re
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, NameObject

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

r = PdfReader(sys.argv[1])
if r.is_encrypted:
    r.decrypt("")
w = PdfWriter(clone_from=r)
root = w._root_object
xfa = root["/AcroForm"]["/XFA"]

new = ArrayObject()
for i in range(0, len(xfa), 2):
    name, ref = xfa[i], xfa[i + 1]
    if str(name) == "form":            # saved form state -> drop so Reader re-merges from datasets
        continue
    if str(name) == "datasets":
        s = ref.get_object()
        xml = s.get_data().decode("utf-8")
        for k, v in DATA.items():
            # match empty <k/> OR existing <k>...</k>
            pat = re.compile(r"<%s\s*/>|<%s\s*>.*?</%s\s*>" % ((re.escape(k),) * 3), re.S)
            if not pat.search(xml):
                print("WARNING: field not in datasets:", k); continue
            xml = pat.sub(lambda m: f"<{k}>{escape(v)}</{k}>", xml, count=1)
        ET.fromstring(xml)              # must still be valid XML
        s.set_data(xml.encode("utf-8"))
    new += [name, ref]
root["/AcroForm"][NameObject("/XFA")] = new

for key in ("/Perms",):                 # usage-rights signature is invalid after editing
    if key in root:
        del root[key]
w.write(sys.argv[2])

# verify
x = PdfReader(sys.argv[2]).trailer["/Root"]["/AcroForm"]["/XFA"]
d = {str(x[i]): x[i + 1].get_object().get_data() for i in range(0, len(x), 2)}
f = ET.fromstring(d["datasets"]).find(".//form1")
print("packets:", list(d), "| filled:", sum(bool((c.text or "").strip()) for c in f), "/", len(f))
