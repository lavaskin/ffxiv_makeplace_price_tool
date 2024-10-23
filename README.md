# FFXIV MakePlace Housing Price Tool

Fetches relevant housing item prices and tallies them up given a MakePlace house item list from the MakePlace app.

## How To Use

- Install all the packages in the packages section below.
- Create a ```.env``` file in the root of this project, and fill out all the information specified in ```.env.example```.
- Run the tool with python and the following parameters:
	- <home_file_list>:  The name of the save, not the file. For example, if the file is named ```test_home_2.list.txt```, input ```test_home_2```.
	- <data_center>: The data center to fetch prices from. Should look like: Aether, Crystal, Etc...
- Example Run: ```python app.py <home_list_file> <data_center>```

## Packages

- [requests](https://pypi.org/project/requests/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

## Links

- [MakePlace](https://makeplace.app/places): For getting house item lists
- [Universalis Api](https://docs.universalis.app): For the pricing data API
- [XIV Item Dump](https://raw.githubusercontent.com/ffxiv-teamcraft/ffxiv-teamcraft/master/libs/data/src/lib/json/items.json): For local item ID lookup
