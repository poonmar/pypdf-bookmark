import logging
from pypdf import PdfReader
from pypdf import PdfWriter
import outline


def main():
    path = input('File Name: ')
    writer = PdfWriter(PdfReader(path))
    #reader = PdfReader(path)
    outline.import_bookmarks(writer, 'bookmarks.json')
    writer.write('output.pdf')
#    outline.export_bookmarks(PdfReader('output.pdf'), 'output.json')


if __name__ == '__main__':
    main()