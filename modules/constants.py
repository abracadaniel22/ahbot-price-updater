"""
constants module - constants and utility methods
@author Abracadaniel22
"""
import os

PREFIX_DATE_FORMAT = "%Y-%m-%d-%H%M%S"

_script_dir = os.path.dirname(os.path.abspath(__file__))
_relative_download_dir = "../etc/data/downloads"
downloads_dir = os.path.join(_script_dir, _relative_download_dir)

def get_download_file_path(filename):
    return os.path.join(downloads_dir, filename)