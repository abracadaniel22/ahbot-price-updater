# AHBot Price Updater

Downloads and parsers auctioneer data file and populate the tables used by mod-ah-bot for AzerothCore.

This requires Abracadaniel22's fork of mod-ah-bot https://github.com/abracadaniel22/mod-ah-bot .

This script works by populating the `ac_world.mod_ahbot` table with the minimum bid price of all items found in the auctioneer data file. The AHBot will use those prices to create auctions and buy your auctions, ultimately simulating the real world with real world data (depending on where you get your auctioneer data file from).

## Installation

- Install docker via https://docs.docker.com/engine/install

- Clone repository

```
git clone https://github.com/abracadaniel22/ahbot-price-updater.git
```

- Build image

```
./build.sh
```

## Configuration

- Configure app by copying `config.conf.dist` to `config.conf` and edit settings


## Run

- Run via docker, mounting the `etc` folder so the VM can read configuration files and write data to a data dir

```
docker run -t -v /path/to/ahbot-price-updater/etc:/usr/src/app/etc ahbotpriceupdater:latest
```

## Configuration profiles

- It is possible to have additional configuration profiles in the config file other than the `default`. Just add new sections to the config file, for example:

```
[my_other_server]
url = https://my_other_server_url
keep_downloads = false
insert_duplicate_behaviour = ignore
```

- To make the script use my_other_server, just set the environment variable `CONFIG_PROFILE`, like the following example:

```
docker run -t -e CONFIG_PROFILE="my_other_server" -v /path/to/ahbot-price-updater/etc:/usr/src/app/etc ahbotpriceupdater:latest
```
