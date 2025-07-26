"""
appdata module - holds application state
@author Abracadaniel22
"""
from typing import Dict, Type, Union
import os

from .typed_config import TypedConfig

_schema: Dict[str, Type[Union[str, int, float, bool]]] = {
    'last_file_name': str
}

def _get_file():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "../etc/data")
    data_file = os.path.join(data_dir, "appdata")
    if not os.path.exists(data_file):
        os.makedirs(data_dir, exist_ok=True)
        with open(data_file, 'w') as fp:
            fp.write("[default]")
    return data_file

appdata = TypedConfig(_get_file(), _schema)