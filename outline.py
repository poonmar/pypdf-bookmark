from pypdf import PdfWriter, PdfReader
from pypdf.generic import Fit
import json

class Importer:

    def __init__(self, writer: PdfWriter = None):
        if writer is None:
            self.writer = PdfWriter()
        else:
            self.writer = writer

    def get_fit(self, items: dict) -> Fit:
        
        fit_type = items.get('type')
        types = {
            'XYZ': Fit.xyz(items.get('left'), items.get('top'), items.get('zoom')),
            'Fit': Fit.fit(),
            'FitH': Fit.fit_horizontally(items.get('top')),
            'FitV': Fit.fit_vertically(items.get('left')),
            'FitR': Fit.fit_rectangle(items.get('left'), items.get('bottom'), items.get('right'), items.get('top')),
            'FitB': Fit.fit_box(),
            'FitBV': Fit.fit_box_vertically(items.get('left'))
        }
        return types.get(fit_type, Fit.fit())


    def add_outlines(self, entries: list, parent=None):
        for entry in entries:
            outline_ref = self.writer.add_outline_item(
                                                    entry['title'],
                                                    entry['page'] - 1,
                                                    parent,
                                                    color=None,
                                                    bold=entry.get('bold'),
                                                    italic=entry.get('italic'),
                                                    fit=self.get_fit(entry),
                                                    is_open=entry.get('is-open', False)
                                                )
            if children := entry.get('children'):
                self.add_outlines(children, outline_ref)

    def import_bookmarks(self, path: str):
        with open(path) as file:
            outline_items = json.load(file)
        #parser.verify(outline_items)
        self.add_outlines(outline_items)

class Exporter:

    def __init__(self, reader: PdfReader):
        self.reader = reader

    def build_tree(self, vals: list) -> list:
        lst = []
        for item in vals:
            if isinstance(item, list):
                prev['children'] = self.build_tree(item)
            else:
                prev = {
                        'title': item.title,
                        'page': self.reader._get_page_number_by_indirect(item.page)
                        }

                attr = {'color': item.color, 'bold': item.bold, 'type': item.type, 'is-open': item.is_open}
                for key, val in attr.items():
                    if val:
                        prev[key] = val
                lst.append(prev)
        return lst

    def export_bookmarks(self, path: str):
        with open(path, 'w') as file:
            json.dump(self.build_tree(self.reader.outline), file, indent=1)
    
def main():
    path = input('File Name: ')
    importer = Importer()
    importer.writer.append(PdfReader(path), import_outline=False)
    importer.import_bookmarks('bookmarks.json')
    importer.writer.write('output.pdf')

    exporter = Exporter(PdfReader('output.pdf'))
    exporter.export_bookmarks('output.json')


if __name__ == '__main__':
    main()
