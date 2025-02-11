import sys
import json
import jsonschema
import logging
import outline

CONTAINS = ['title', 'page']
TYPES = {'title': str,
         'page': int,
         'parent': list,
         'color': tuple[int, int, int],
         'bold': bool,
         'italic': bool,
         'type': str,
         'is_open': bool
        }

def validate_entry(entry: dict) -> str:
    for attr in CONTAINS:
        if attr not in entry:
            return f'Missing attribute: {attr}'
    for key, item in entry.items():
        if key not in TYPES:
            return f'{key} is not a valid attribute!'
        elif not isinstance(item, TYPES[key]):
            return f'{item} is not of type {str(TYPES[key])}!'





