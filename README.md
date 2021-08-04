# PDF Extractor
A short and sweet script to read, decrypt and pull certain pages from
a PDF. I was having to do this task often via a long winded process as
I don't own a paid PDF editor that supports this functionality.

## Usage
```
usage: extract.py [-h] [-s None] path pages

:param path: the path to the PDF file
:param pages: a string of comma and hyphen separated page numbers e.g. 1,3-6 == 1,3,4,5,6
:param suffix: the suffix to append to the filename when saving. If None, will use 'pages'.
:return: None

positional arguments:
  path                  The path of the PDF to take a subset of
  pages                 The pages in comma or hyphen-separated values

optional arguments:
  -h, --help            show this help message and exit
  -s None, --suffix None
                        The suffix to append to the save file
```

### Examples
```shell
python3 extract.py some_doc.pdf 1,2,3
python3 extract.py some_doc.pdf 1-3
python3 extract.py some_doc.pdf 1,2,3-5 -s "somesuffix"
```

## Alias
For speed of access, you can also alias this script depending on your OS.

Append the following to the end of your shell configuration profile file (`.zshrc`, `.bashrc`, etc.) and save:
```shell
alias pdfext="python3 extract.py"
```

You should then be able to run a more simplified command:
```shell
pdfext some_doc.pdf 1,2,3
pdfext some_doc.pdf 1-3
pdfext some_doc.pdf 1,2,3-5 -s "somesuffix"
```