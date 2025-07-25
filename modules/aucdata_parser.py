"""
aucdataparser module - parses auctioneer file
depends on lua5.3 installed in the system
@author Abracadaniel22
"""
import re
import tempfile
import subprocess
import json
import os

def _eval_lua_to_json(lua_table_str):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.lua', delete=False) as f:
        lua_path = f.name
        f.write(f"""
local json = require("dkjson")
local data = {lua_table_str}
print(json.encode(data))
        """)
    try:
        result = subprocess.run(["lua5.3", lua_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
        os.remove(lua_path)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Lua error: {e.stderr} \nlua_table_str: {lua_table_str}\nlua_path: {lua_path}") from e

def _parse_aucdata_file(aucdata_file):
    with open(aucdata_file, 'r', encoding='utf-8') as f:
        content = f.read()
    table_data = re.search(r"AucScanData\s*=\s*(\{.*\})", content, re.DOTALL)
    if not table_data:
        raise ValueError("Failed to extract Lua table from input")
    return _eval_lua_to_json(table_data.group(1))

def _eval_auction_block(lua_block):
    if lua_block.strip().startswith("return"):
        lua_block = lua_block.strip()[6:].strip()
    return _eval_lua_to_json(lua_block)

def parse_auctions(aucdata_file):
    data = _parse_aucdata_file(aucdata_file)
    first_server = next(iter(data['scans'].values()))
    first_faction = next(iter(first_server.values()))
    ropes = first_faction['ropes']

    item_prices = {}

    for rope in ropes:
        auctions = _eval_auction_block(rope)
        for fields in auctions:
            try:
                item_link = fields[0]
                item_name = fields[8]
                min_bid = int(fields[14])
                current_bid = int(fields[5])
                buyout = int(fields[16])
                item_id = int(item_link.split(':')[1])

                if item_id not in item_prices:
                    item_prices[item_id] = {
                        'name': item_name,
                        'min_prices': [],
                        'max_prices': [],
                        'bid_prices': []
                    }
                if buyout > 0:
                    item_prices[item_id]['min_prices'].append(buyout)
                elif min_bid > 0:
                    item_prices[item_id]['min_prices'].append(min_bid)

                if buyout > 0:
                    item_prices[item_id]['max_prices'].append(buyout)
                elif current_bid > 0:
                    item_prices[item_id]['max_prices'].append(current_bid)
                    
                if current_bid > 0:
                    item_prices[item_id]['bid_prices'].append(current_bid)
            except Exception as e:
                raise RuntimeError(str(fields)) from e
    
    return item_prices