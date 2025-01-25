import json
import jsonschema
import difflib
import logging
from pypdf.generic import Fit

logger = logging.getLogger(__name__)

def validate_json(input: dict) -> bool:
    pass

def parse(path: str) -> list:

    items = json.load(path)
    
    jsonschema.validate(items)

    return items


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

