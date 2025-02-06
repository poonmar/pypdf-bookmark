from pypdf import PdfWriter, PdfReader
from pypdf.generic import Fit
import parser
import logging

logger = logging.getLogger(__name__)
def get_fit(items: dict) -> Fit:
    
    fit_type = items.get('Type')
    types = {
         'XYZ': Fit.xyz(items.get('Left'), items.get('Top'), items.get('Zoom')),
         'Fit': Fit.fit(),
         'FitH': Fit.fit_horizontally(items.get('Top')),
         'FitV': Fit.fit_vertically(items.get('Left')),
         'FitR': Fit.fit_rectangle(items.get('Left'), items.get('Bottom'), items.get('Right'), items.get('Top')),
         'FitB': Fit.fit_box(),
         'FitBV': Fit.fit_box_vertically(items.get('Left'))
    }
    
    if fit_type not in types.keys():
        logger.warning('Fit type is invalid. Using the default fit instead.')

    return types.get(fit_type, Fit.DEFAULT_FIT)


def create_outlines(writer: PdfWriter, entries: dict):
    for item in entries:
        outline_ref = writer.add_outline_item(item['title'], item['page'], item.get('parent'), color=item.get('color'), bold=item.get('bold'), fit=get_fit(item), is_open=item.get('is-open', True))
        if children := item.get('children'):
            for child in children:
                create_outlines(writer, child)


def import_bookmarks(writer: PdfWriter, path: str):
    outline_items = parser.parse(path)
    parser.verify(outline_items)
    create_outlines(writer, outline_items)

def export_bookmarks(reader: PdfReader, path: str):
    output = parser.to_json(reader)
    with open(path, 'w') as file:
        file.write(output)