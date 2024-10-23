# FFXIV MakePlace Housing Price Tool

Fetches relevant housing item prices and tallies them up given a MakePlace house item list form the MakePlace app.

Reads item data from ```items_db.json``` to then fetch prices from Universalis. Saves item prices for 24 hours, and then refetches.

Probably will break if there are items in the home file that aren't on the market board. I don't do enough testing.

## How To

- In the ```/homes``` folder, place a MakePlace item list from the app. Remove everything outside of the furnishing list, dyes are not currently supported.
- Run the app with python and the parameter of the item list name, for example: ```python3 app.py test_home.txt```.

## Links

- [MakePlace](https://makeplace.app/places): For getting house item lists
- [XIVApi](https://xivapi.com/docs/Search#search): For item information
- [Universalis Api](https://docs.universalis.app): For Pricing Data
- [XIV World Data Dump](https://github.com/xivapi/ffxiv-datamining/blob/master/csv/World.csv): For use in the Universalis API for where to look for prices
- [XIV Item Dump](https://raw.githubusercontent.com/ffxiv-teamcraft/ffxiv-teamcraft/master/libs/data/src/lib/json/items.json): For item ID lookup