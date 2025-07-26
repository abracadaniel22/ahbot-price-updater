"""
config module - reads user configuration
@author Abracadaniel22
"""
from typing import Dict, Type, Union
import os

from .typed_config import TypedConfig

_schema: Dict[str, Type[Union[str, int, float, bool]]] = {
    'url': str,
    'skip_download': bool,
    'keep_downloads': bool,
    'insert_duplicate_behaviour': str,
    'mysql_host': str,
    'mysql_port': str,
    'mysql_user': str,
    'mysql_password': str,
    'mysql_database': str
}

def _get_file():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    conf_dir = os.path.join(script_dir, "../etc/conf")
    config_dist_file = os.path.join(conf_dir, "config.conf.dist")
    config_file = os.path.join(conf_dir, "config.conf")
    if os.path.exists(config_file):
        return config_file
    elif os.path.exists(config_dist_file):
        return config_dist_file
    else:
        raise RuntimeError(f"None of the config files are found: [{config_file}] or [{config_dist_file}].")

section = "default"
if "CONFIG_PROFILE" in os.environ:
    section = os.environ["CONFIG_PROFILE"]
config = TypedConfig(_get_file(), _schema, section=section)
