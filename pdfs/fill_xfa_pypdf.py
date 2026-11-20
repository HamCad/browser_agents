#!/usr/bin/env python3
"""pypdf-only variant. usage: fill_xfa_pypdf.py in.pdf out.pdf  (AES-encrypted input needs 'cryptography' or 'pycryptodome')"""
import sys, re
from xml.sax.saxutils import escape
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject
import os
# reuse DATA dict from fill_xfa.py without running it
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fill_xfa.py')).read()
ns = {}; exec("P1=" + src.split("P1 = ")[1].split("DATA = ")[0] + "DATA = " + src.split("DATA = ")[1].split("pdf = pikepdf")[0], {'__builtins__': __builtins__}, ns)
DATA = ns['DATA']

r = PdfReader(sys.argv[1])
if r.is_encrypted: r.decrypt("")             # empty user password
w = PdfWriter(clone_from=r)                  # clone keeps XFA/AcroForm
xfa = w._root_object["/AcroForm"]["/XFA"]
for i in range(0, len(xfa), 2):
    if str(xfa[i]) == "datasets":
        s = xfa[i + 1].get_object()
        xml = s.get_data().decode("utf-8")
        for k, v in DATA.items():
            pat = re.compile(r"<%s\s*/>" % re.escape(k)); assert pat.search(xml), k
            xml = pat.sub(lambda m: f"<{k}>{escape(v)}</{k}>", xml, count=1)
        s.set_data(xml.encode("utf-8"))
if "/Perms" in w._root_object: del w._root_object["/Perms"]
w.write(sys.argv[2]); print("wrote", sys.argv[2])
