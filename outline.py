from pypdf import PdfWriter
import parser

def create_outline(writer: PdfWriter, items: dict):
    
    outline_ref = writer.add_outline_item(items['Title'], items['Page'], items.get('Parent'), color=items.get('Color'), bold=items.get('Bold'), fit=parser.get_fit(items), is_open=items.get('Is Open', True))
    return outline_ref
    