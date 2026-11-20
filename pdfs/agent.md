This PDF is a pure XFA form. It has zero AcroForm fields, so
standard PDF form-filling tools and skills will not work. Don't use them,
and don't use OCR, overlays, or flattening.

Instead, fill it by editing the XFA data XML inside the PDF:

1. Open the PDF with pypdf (or pikepdf). It is AES-encrypted with an empty
   user password, so call reader.decrypt("") first. If decryption fails
   because no crypto library is installed, tell me.
2. Go to Root -> AcroForm -> XFA. It is an array of [name, stream, name,
   stream, ...]. Find the stream named "datasets".
3. Read that stream's XML. It has empty elements under <form1>, like
   <award/>. The data is flat, so there are no Page1/Page2 wrappers.
4. Replace each empty element with <fieldname>text</fieldname>. XML-escape
   & < >. Multi-line fields take literal newlines. The 12 fields are: award,
   category, awardPeriod, rankName, majcom_foa_dru, DAFSC, nomineeTelephone,
   officeAddress, rank, specificAccomplishments, p2Name,
   p2SpecificAccomplishments.
5. Write the new XML back into the stream (stream.set_data(...) in pypdf).
6. Delete Root["/Perms"]. Editing breaks the usage-rights signature.
7. Save the PDF, then re-read it to confirm the datasets XML parses and
   every field has a value.

Use obviously synthetic data. Note that you cannot render XFA in the
sandbox, so verify the data XML, not the visuals. A working script is
attached (fill_xfa_pypdf.py). Run it first, and edit its DATA dict for
different values.
