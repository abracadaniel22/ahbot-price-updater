"""
AHBot price updater
Downloads an auctioneer data file and inserts the minimum bid price of every item into the AHBot table to be used in-game
@author Abracadaniel22
"""
from collections import Counter
import sys, os

from modules.downloader import download_new_file, DownloadStatus
from modules.aucdata_parser import parse_auctions
from modules.repository import Repository, InsertResult
from modules.appdata import appdata
from modules.config import config
from modules import constants
from modules.file_comparator import are_files_equal

def _is_new_file(new_file_name):
    if appdata.last_file_name is not None:
        return not are_files_equal(constants.get_download_file_path(appdata.last_file_name), constants.get_download_file_path(new_file_name))
    return True

def _main():
    print("Downloading...")
    if config.skip_download:
        if appdata.last_file_name is None:
            print("Can't skip download without a previously downloaded file.")
            sys.exit(1)
        aucdata_file = appdata.last_file_name
    else:
        download_result = download_new_file()
        if download_result.status == DownloadStatus.SKIPPED:
            print("Download skipped")
            return
        aucdata_file = download_result.file
        print(f"Successfully downloaded {aucdata_file}")
        if not _is_new_file(aucdata_file):
            print(f"Downloaded file unchanged. Skipping. Latest file remains {appdata.last_file_name}")
            return

    print("Parsing...")
    item_prices = parse_auctions(constants.get_download_file_path(aucdata_file))

    if config.keep_downloads:
        appdata.last_file_name = aucdata_file
    elif aucdata_file is not None:
        print(f"Deleting downloaded file {aucdata_file}...")
        os.remove(constants.get_download_file_path(aucdata_file))

    print("Connecting to the database...")
    repository = Repository()
    stats = Counter()

    upsert = True
    if config.insert_duplicate_behaviour == 'ignore':
        upsert = False
    print(f"Updating table. Existing items will be {'overwritten' if upsert else 'ignored'}...")
    for item_id, data in item_prices.items():
        if not data['min_prices'] or not data['max_prices']:
            continue
        min_bid_price = min(data['min_prices'])
        if upsert:
            result = repository.upsert(item_id, min_bid_price)
        else:
            result = repository.insert_ignore(item_id, min_bid_price)
        stats[result.name] += 1
    
    get_stat = lambda result_type: stats.get(result_type.name, 0)
    print(f"{len(item_prices)} items processed. {get_stat(InsertResult.INSERTED)} new items inserted. {get_stat(InsertResult.UPDATED)} rows updated. {get_stat(InsertResult.KEPT_SAME)} rows kept same. {repository.count()} total items now in the table.")

if __name__ == "__main__":
    _main()
