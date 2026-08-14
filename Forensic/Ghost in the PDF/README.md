# Ghost in the PDF

**Category:** Forensics

**Difficulty:** Medium

**Points:** 200

**Author:** Bilawal Ali

**Event:** AccessDenied CTF 2026

## Challenge Description

Ek cyber investigation ke dauran team ko ek suspicious PDF file mili jo pehli nazar mein bilkul normal lag rahi thi. File kholne par sirf ek simple document nazar aaya, lekin forensic analysis ne kuch aur hi kahani bayan ki.
Maloom hua ke hacker ne apna message ek hi jagah par nahi chhupaya, balkay PDF ki mukhtalif layers mein tod kar chhupa diya hai. Kuch nishaan page ke andar hain, kuch document ki apni information mein, aur kuch woh cheezen hain jo shayad peeche reh gayi hain.
Ab aapka mission hai ke is PDF ko forensic nazar se analyze karo, har hidden fragment ko recover karo, unhein combine karo, aur hacker ke chhupaye hue final flag tak pohancho.

**Flag format:** `MUET{...}`

## Provided File

```text
forensics102_layers.pdf
```

## Solution

The challenge requires examining the PDF beyond its rendered content. Four fragments of the flag are hidden in different locations within the file.

The investigation can be divided into four stages:

1. Visible page content
2. Document metadata
3. Embedded file
4. Data appended after the `%%EOF` marker

### 1. Visible Page Content

The first step is to extract the text from the PDF.

Using `pypdf`:

```bash
python3 -c "from pypdf import PdfReader; print(PdfReader('forensics102_layers.pdf').pages[0].extract_text())"
```

The output contains:

```text
MUET{Dikha_
fragment 1 of 4
Forensics 102 - Layers Within Layers
AccessDenied CTF Team
```

The visible content provides the first fragment:

```text
MUET{Dikha_
```

The message `fragment 1 of 4` indicates that additional fragments are hidden elsewhere in the document.

### 2. Document Metadata

The next step is to inspect the raw PDF structure.

```bash
strings forensics102_layers.pdf
```

The output reveals the PDF's internal objects and metadata.

The `/Subject` field contains:

```text
/Subject (S3VjaF9BdXJf)
```

This value is Base64 encoded.

Decode it with Python:

```bash
python3 -c "import base64; print(base64.b64decode('S3VjaF9BdXJf').decode())"
```

Output:

```text
Kuch_Aur_
```

The second fragment is:

```text
Kuch_Aur_
```

### 3. Embedded File

The PDF also contains an embedded file referenced through the `/Names` and `/EmbeddedFiles` structures.

The embedded file is:

```text
case_notes.txt
```

Its contents include:

```text
Case notes:
Analyst observed unusual byte patterns near the xref table.
Recovered fragment (hex-encoded):
4d696c615f
```

The hexadecimal value can be decoded using:

```bash
python3 -c "print(bytes.fromhex('4d696c615f').decode())"
```

Output:

```text
Mila_
```

The third fragment is:

```text
Mila_
```

### 4. Data After `%%EOF`

The final stage is to inspect the end of the PDF file.

PDF readers normally stop processing after the final `%%EOF` marker. Data appended after this marker may therefore remain hidden from the normal document view.

Inspecting the file reveals:

```text
%%EOF
% ---------------------------------------------
% Internal QA note - do not ship to client
% fragment4(rot13): Xhpu_Nhe}
% ---------------------------------------------
```

The fragment is encoded using ROT13.

Decode it with:

```bash
python3 -c "import codecs; print(codecs.decode('Xhpu_Nhe}', 'rot13'))"
```

Output:

```text
Kuch_Aur}
```

The fourth fragment is:

```text
Kuch_Aur}
```

## Flag Reconstruction

The recovered fragments are:

| Fragment | Location             | Encoding    | Value         |
| -------- | -------------------- | ----------- | ------------- |
| 1        | Visible page content | Plaintext   | `MUET{Dikha_` |
| 2        | Document metadata    | Base64      | `Kuch_Aur_`   |
| 3        | Embedded file        | Hexadecimal | `Mila_`       |
| 4        | Data after `%%EOF`   | ROT13       | `Kuch_Aur}`   |

Combining the fragments in order:

```text
MUET{Dikha_ + Kuch_Aur_ + Mila_ + Kuch_Aur}
```

produces:

```text
MUET{Dikha_Kuch_Aur_Mila_Kuch_Aur}
```

## Flag

```text
MUET{Dikha_Kuch_Aur_Mila_Kuch_Aur}
```

## Tools Used

* `strings` — raw PDF content inspection
* `pypdf` — PDF parsing and text extraction
* Python — Base64, hexadecimal, and ROT13 decoding
* PDF structure analysis — metadata and embedded file inspection

## Key Takeaways

PDF files should not be analyzed solely through their rendered content. Important forensic artifacts may exist within the underlying file structure.

During PDF analysis, useful areas to examine include:

1. Visible page content and content streams
2. Document metadata and Info dictionaries
3. XMP metadata
4. Embedded files and `/EmbeddedFiles`
5. PDF objects and streams
6. Data appended after the final `%%EOF` marker

This challenge demonstrates how a single document can contain multiple layers of information that are not immediately visible to the user.
