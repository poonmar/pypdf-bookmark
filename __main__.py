import logging
from pypdf import PdfReader
from pypdf import PdfWriter
import outline


def main() -> None:

    path = input('File Name: ')
    writer = PdfWriter()
    reader = PdfReader(path)
    outline.import_outline(writer, 'bookmarks.json')
    writer.write('output.pdf')


if __name__ == '__main__':
    main()