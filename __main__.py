from pypdf import PdfReader
from pypdf import PdfWriter
import outline
import parser


def main() -> None:

    path = input('File Name: ')
    writer = PdfWriter()
    reader = PdfReader(path)
    outline_items = parser.parse(path)
    ids = set()
    outline_refs = []

    for item in outline_items:
        id = item.get('id')
        if id is not None:
            if id in ids:
                pass
            else:
                ids.add(id)
    
    while j p[;]
    



if __name__ == '__main__':
    main()