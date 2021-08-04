#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A short and sweet script to read, decrypt and pull certain pages from a PDF
"""
__author__ = "David Klein"
__copyright__ = "Copyright 2021, David Klein"
__credits__ = ["David Klein"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "David Klein"
__status__ = "Production"

import getpass
import os
import typing

import PyPDF2
import plac
from tqdm import tqdm


def parse_page_arg(pages: str) -> set:
    """
    Parse a complete list of page numbers from the page argument provided
    :param pages: a string of comma and hyphen separated page numbers e.g. 1,3-6 == 1,3,4,5,6
    :return: a set of page numbers
    """
    all_pages = set()
    if not isinstance(pages, str):
        raise TypeError(f"Pages argument must be a string but is a '{type(pages)}'")

    for page in pages.split(","):
        page = page.strip()
        if page != "":
            if page.isnumeric():
                all_pages.add(int(page))

            elif "-" in page:
                page_a, page_b = page.split("-", 1)
                page_a = page_a.strip()
                page_b = page_b.strip()
                if page_a.isnumeric() and page_b.isnumeric():
                    all_pages.update(set(range(int(page_a), int(page_b)+1)))
                else:
                    raise ValueError(f"'{page}' is not a valid page format in '{pages}'")

            else:
                raise ValueError(f"'{page}' is not a valid page format in '{pages}'")

    return all_pages


@plac.annotations(
    path=plac.Annotation("The path of the PDF to take a subset of", "positional", None, str),
    pages=plac.Annotation("The pages in comma or hyphen-separated values", "positional", None, str),
    suffix=plac.Annotation("The suffix to append to the save file", "option", "s", str),
)
def main(
    path: typing.Union[os.PathLike, str],
    pages: str,
    suffix: typing.Optional[str] = None
) -> None:
    """
    :param path: the path to the PDF file
    :param pages: a string of comma and hyphen separated page numbers e.g. 1,3-6 == 1,3,4,5,6
    :param suffix: the suffix to append to the filename when saving. If None, will use 'pages'.
    :return: None
    """
    # Parse page numbers
    page_nums = parse_page_arg(pages)

    # Create save path
    base, ext = os.path.splitext(path)
    if not suffix:
        suffix = pages
    wpath = base + "_" + suffix + ext

    # Open PDF for reading
    print(f"Opening '{path}' for reading and '{wpath}' for writing")
    with open(path, 'rb') as rf, open(wpath, 'wb') as wf:
        reader = PyPDF2.PdfFileReader(rf)
        writer = PyPDF2.PdfFileWriter()

        # Decrypt if needed
        if reader.isEncrypted:
            pwd = getpass.getpass("This PDF is encrypted. Please enter a password to decrypt: ")
            res = reader.decrypt(pwd)
            if res == 0:
                raise ValueError("Provided password does not match")

        # Iterate through pages in order
        for n in tqdm(sorted(list(page_nums)), "Extracting pages", unit="pages"):
            page = reader.getPage(n-1)  # Page indicies start at zero, normal page numbering starts at 1
            writer.addPage(page)

        # Copy encryption of input file
        if reader.isEncrypted:
            writer.encrypt(pwd)

        # Write pages to new file
        writer.write(wf)
        print(f"Finished saving pages {page_nums} from '{path}' to '{wpath}'")


if __name__ == "__main__":
    plac.call(main)
