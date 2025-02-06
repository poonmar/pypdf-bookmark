import sys
import json
import jsonschema
import logging
import outline

logger = logging.getLogger(__name__)
logging.basicconfig(filename=sys.stderr, level=logging.WARNING)

def validate_json(input: dict) -> bool:
    pass

def from_json(path: str) -> list:

    try:
        items = json.load(path)
    except json.JSONDecodeError as err:
        logger.critical('Invalid JSON File!')
    return items



def build_tree(vals: list) -> list:
    lst = []
    for item in vals:
        if isinstance(item, list):
            prev['children'] = build_tree(item, prev)
        else:
            lst.append({'title': item.title, 'page': item.page, 'color': item.color, 'bold': item.bold, 'type': item.type, 'is-open': item.is_open})
        prev = item 
    return lst

def to_json(reader) -> str:
    outlines = reader.outline
    return json.dump(build_tree(outlines))




