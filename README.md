# FFXIV MakePlace Housing Price Tool

Fetches relevant housing item prices and tallies them up given a MakePlace house item list from the MakePlace app. This currently only supports english, but could change in the future.

## How To Use

- Install all the packages in the packages section below.
- Create a ```.env``` file in the root of this project, and fill out all the information specified in ```.env.example```.
- Run the tool with python and the following parameters:
	- <home_list_file> (Required):  The name of the save, not the file. For example, if the file is named ```test_home_2.list.txt```, input ```test_home_2```.
	- <data_center> (Optional): The data center to fetch prices from. Should look like: Aether, Crystal, Etc...
	- <gil_cutoff> (Optional): The amount in an item has to be under to be included in the running total. For if you want to exlude the 4 million Gil tonberry statue.
- Example Runs:
	- ```python app.py <home_list_file>```
	- ```python app.py <home_list_file> <data_center>```
	- ```python app.py <home_list_file> <data_center> <gil_cutoff>```
	- ```python app.py <home_list_file> <gil_cutoff> <data_center>```
	- ```python app.py <home_list_file> <gil_cutoff>```
- Optionally, if you don't want to open your MakePlace Save folder, you can use: ```python app.py list``` and it will print out all the available house saves you can reference for the above commands.
	- The "list" argument only works if no other arguments are supplied.

## Packages

- [requests](https://pypi.org/project/requests/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [chardet](https://pypi.org/project/chardet/)
- [termcolor](https://pypi.org/project/termcolor/)

## Known Issues

- Local prices ignore DC. So if you fetch a bunch from Aether, and then query from Crystal, it'll use the same local prices.
	- Workaround: Delete the local ```data/item_prices.json``` file to get new prices for the new DC.
- There are probably more items that don't exist in the ```data/item_db.json``` file that could cause problems. Currently an error is printed so this shouldn't be an issue, but could possibly cause some weird edge case.
	- If you know of any more that could be missing, add them to the ```src/local.py > excluded_items_list``` array.

## Links

- [MakePlace](https://makeplace.app/places): For getting house item lists
- [Universalis Api](https://docs.universalis.app): For the pricing data API
- [XIV Item Dump](https://raw.githubusercontent.com/ffxiv-teamcraft/ffxiv-teamcraft/master/libs/data/src/lib/json/items.json): For local item ID lookup
