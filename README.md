# AHBot Price Updater

Downloads and parsers auctioneer data file and populate the tables used by mod-ah-bot for AzerothCore.

This requires Abracadaniel22's fork of mod-ah-bot https://github.com/abracadaniel22/mod-ah-bot .

This script works by populating the `ac_world.mod_ahbot` table with the minimum bid price of all items found in the auctioneer data file.

## Installation

- Install docker via https://docs.docker.com/engine/install

- Clone repository

```
git clone https://github.com/abracadaniel22/ahbot-price-updater.git
```

- Configure app by copying `config.conf.dist` to `config.conf`

- Build image

```
./build.sh
```

## Run

- Run via docker, mounting the `etc` folder so the VM can read configuration files and write data to a data dir

```
docker run -v /path/to/ahbot-price-updater/etc:/usr/src/app/etc ahbotpriceupdater:latest
```