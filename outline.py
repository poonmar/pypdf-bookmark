from pypdf import PdfWriter, PdfReader
from pypdf.generic import Fit
import parser
import json

def get_fit(items: dict) -> Fit:
    
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


def create_outlines(writer: PdfWriter, entries: list, parent=None):
    for entry in entries:
        outline_ref = writer.add_outline_item(
                                                entry['title'],
                                                entry['page'] - 1,
                                                parent,
                                                color=entry.get('color'),
                                                bold=entry.get('bold'),
                                                italic=entry.get('italic'),
                                                fit=get_fit(entry),
                                                is_open=entry.get('is-open', False)
                                            )
        if children := entry.get('children'):
            create_outlines(writer, children, outline_ref)

def build_tree(vals: list) -> list:
    lst = []
    for item in vals:
        if isinstance(item, list):
            prev['children'] = build_tree(item)
        else:
            prev = {
                    'title': item.title,
                    'page': item.page
                    #'color': item.color,
                    #'bold': item.bold,
                    #'type': item.typ,
                    #'is-open': item.is_open
                    }
            lst.append(prev)
    return lst

def import_bookmarks(writer: PdfWriter, path: str):
    with open(path) as file:
        outline_items = json.load(file)
    #parser.verify(outline_items)
    create_outlines(writer, outline_items)

def export_bookmarks(reader: PdfReader, path: str):
    with open(path, 'w') as file:
        json.dump(build_tree(reader.outline), file)