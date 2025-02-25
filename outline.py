from pypdf import PdfWriter, PdfReader
from pypdf.generic import Fit, Destination
import json

class Importer:

    def __init__(self, writer: PdfWriter = None):
        if writer is None:
            self.writer = PdfWriter()
        else:
            self.writer = writer
    
    def _parse_color(self, color):
        if isinstance(color, list):
            return tuple([value / 255 for value in color])
        return color
    
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
                                                    color=self._parse_color(entry.get('color')),
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
        self.outline = reader.outline

    def _get_font_format(self, outline):
        #1=italic,2=bold,3=both
        formats = {}
        if outline.font_format > 2:
            formats['bold'] = True
        if outline.font_format % 2 == 1:
            formats['italic'] = True
        return formats

    def build_tree(self, vals: list) -> list:
        lst = []
        for item in vals:
            if isinstance(item, list):
                prev['children'] = self.build_tree(item)
            else:
                attrs = {
                        'title': item.title,
                        'page': self.reader._get_page_number_by_indirect(item.page) + 1,
                        'type': item.typ.strip('/'),
                        'zoom': item.zoom if isinstance(item.zoom, int) and item.zoom else None,
                        'left': item.left,
                        'right': item.right,
                        'top': item.top,
                        'bottom': item.bottom,
                        'color': [round(cvals * 255) for cvals in item.color] if item.color != [0.0,0.0,0.0] else None,
                        }
                attrs.update(self._get_font_format(item))
                if item.outline_count:
                    attrs['is-open'] = item.outline_count > 0

                prev = {key: val for key, val in attrs.items() if val is not None}
                lst.append(prev)
        return lst

    def export_bookmarks(self, path: str, indent=4):
        with open(path, 'w') as file:
            json.dump(self.build_tree(self.outline), file, indent=indent)
    
def main():
    #path = input('File Name: ')
    path = ... #filename goes here    
    '''
    importer = Importer()
    importer.writer.append(PdfReader(path), import_outline=False)
    importer.import_bookmarks('bookmarks.json')
    importer.writer.write('output.pdf')
    '''
    #exporter = Exporter(PdfReader(path))
    #exporter.export_bookmarks('output.json')


if __name__ == '__main__':
    main()
