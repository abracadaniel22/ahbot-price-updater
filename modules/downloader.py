"""
downloader module - downloads the acutioneer data from the URL in the config file
@author Abracadaniel22
"""

import os
import requests
from datetime import datetime
from email.utils import parsedate_to_datetime
from enum import Enum, auto
from typing import Optional
from dataclasses import dataclass

from .config import config
from .appdata import appdata
from . import constants

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) "
        "Gecko/20100101 Firefox/127.0"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
        "image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}

class DownloadStatus(Enum):
    DOWNLOADED = auto()
    SKIPPED = auto()

@dataclass
class DownloadResult:
    status: DownloadStatus
    file: Optional[str]

def _get_last_download_date(last_file):
    if last_file:
        last_path = constants.get_download_file_path(last_file)
        if os.path.isfile(last_path):
            return datetime.utcfromtimestamp(os.path.getmtime(last_path))
    return None

def _get_remote_modified_date(head_resp):
    if head_resp.status_code != 200:
        raise Exception(f"HEAD request failed with status {head_resp.status_code}")

    remote_last_modified = head_resp.headers.get("Last-Modified")
    if not remote_last_modified:
        return datetime.utcnow()
    return parsedate_to_datetime(remote_last_modified).astimezone(datetime.utcnow().tzinfo)

def _build_local_file_name(head_resp):
    filename = datetime.utcnow().strftime(constants.PREFIX_DATE_FORMAT)
    cd = head_resp.headers.get("Content-Disposition")
    if cd and "filename=" in cd:
        filename += "-" + cd.split("filename=")[-1].strip().strip('"')
    return filename

def _get_file(url, dest_file, remote_last_modified_dt):
    full_path = os.path.join(constants.downloads_dir, dest_file)
    with requests.get(url, headers=HEADERS, stream=True) as r:
        r.raise_for_status()
        with open(full_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    mod_time = remote_last_modified_dt.timestamp()
    os.utime(full_path, times=(mod_time, mod_time))

def download_new_file() -> DownloadResult:
    url = config.url
    last_file_name = appdata.last_file_name

    head_resp = requests.head(url, headers=HEADERS, allow_redirects=True)

    remote_last_modified_dt = _get_remote_modified_date(head_resp)
    if last_file_name:
        last_modified_local = _get_last_download_date(last_file_name)

        if last_modified_local and remote_last_modified_dt <= last_modified_local:
            return DownloadResult(status = DownloadStatus.SKIPPED, file = None)

    filename = _build_local_file_name(head_resp)
    _get_file(url, filename, remote_last_modified_dt)

    return DownloadResult(status = DownloadStatus.DOWNLOADED, file = filename)
