# FFXIV MakePlace Housing Price Tool

Fetches relevant housing item prices and tallies them up given a MakePlace house item list from the MakePlace app. This currently only supports english, but could change in the future.

## How To Use

- Install all the dependencies with poetry ```poetry install```
- Create a ```.env``` file in the root of this project, and fill out all the information specified in ```.env.example```.
  - MAKEPLACE_SAVES_PATH = The path where all of your <home_name>.list.txt files are located
  - ENABLE_OUTPUT = Whether or not to output a text file containing all the found prices for all the homes items
    - OUTPUT_PATH = Where to output the price list to
- Run the tool with python and the following parameters:
  - <home_list_file> (Required):  The name of the save, not the file. For example, if the file is named ```test_home_2.list.txt```, input ```test_home_2```.
  - <data_center> (Optional): The data center to fetch prices from. Should look like: Aether, Crystal, Etc...
  - <gil_cutoff> (Optional): The amount in an item has to be under to be included in the running total. For if you want to exclude the 4 million Gil tonberry statue.
- Example Runs:
  - ```poetry run python app.py <home_list_file>```
  - ```poetry run python app.py <home_list_file> <data_center>```
  - ```poetry run python app.py <home_list_file> <data_center> <gil_cutoff>```
  - ```poetry run python app.py <home_list_file> <gil_cutoff> <data_center>```
  - ```poetry run python app.py <home_list_file> <gil_cutoff>```
- You can also use the included ```./run``` script and pass arguments to that directly instead
  - ```./run <home_list_file>```
- Optionally, if you don't want to open your MakePlace Save folder, you can use: ```poetry run python app.py list``` and it will print out all the available house saves you can reference for the above commands.
  - The "list" argument only works if no other arguments are supplied.

## Known Issues

- Local prices ignore DC. So if you fetch a bunch from Aether, and then query from Crystal, it'll use the same local prices.
  - Workaround: Delete the local ```data/item_prices.json``` file to get new prices for the new DC.
- There are probably more items that don't exist in the ```data/item_db.json``` file that could cause problems. Currently an error is printed so this shouldn't be an issue, but could possibly cause some weird edge case.
  - If you know of any more that could be missing, add them to the ```src/local.py > excluded_items_list``` array.
- I'm currently manually updating the items_db.json file which is suuuuper dumb. Should be fetching that on some long timestamped interval.

## Contributing

If you want to submit code to the repo, feel free to make a PR targeting the dev branch and @lavaskin will review it.

Feel free to fork or copy code from this project as well.

## Links

- [ReMakePlace](https://github.com/RemakePlace): For the application to generate the housing lists this app consumes
- [Universalis Api](https://docs.universalis.app): For the pricing data API
- [XIV Item Dump](https://raw.githubusercontent.com/ffxiv-teamcraft/ffxiv-teamcraft/master/libs/data/src/lib/json/items.json): For local item ID lookup
