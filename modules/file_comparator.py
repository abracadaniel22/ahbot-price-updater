"""
file_comparator module - utility to hash check files
@author Abracadaniel22
"""
import subprocess
import os

def _get_md5_checksum(filepath):
    try:
        result = subprocess.run(['md5sum', filepath], capture_output=True, text=True, check=True)
        checksum = result.stdout.split(' ')[0]
        return checksum
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error calculating MD5 for {filepath}: {e}") from e
    except FileNotFoundError as e:
        raise RuntimeError(f"Error: md5sum command not found. Ensure it's in your PATH.") from e

def are_files_equal(file1_path, file2_path):
    if not os.path.exists(file1_path) or not os.path.exists(file2_path):
        return False
    return _get_md5_checksum(file1_path) == _get_md5_checksum(file2_path)
