import sys
import json
import time
import os

from lib.item import Item
from lib.api import UniversalisApi


# World Data: https://github.com/xivapi/ffxiv-datamining/blob/master/csv/World.csv
# #   InternalName	Name	    Region  UserType  DataCenter  IsPublic
# 99  Sargatanas	Sargatanas	1	    4	      4	          True
DATA_CENTER: str = 'Aether'
WORLD = 99 # Sargatanas


def load_items_db() -> dict:
	# File Structure: { "ItemId": { "en": "Item Name" }, ... }

	# Load in the raw items databse JSON
	items_dict = {}
	with open('./data/items_db.json', 'r', encoding='utf-8') as file:
		items_dict = json.load(file)
	return items_dict
#end load_items_db

def load_item_prices() -> list[Item]:
	# Try to load in the raw item prices JSON
	# If it fails, return an empty dictionary
	try:
		with open('./data/item_prices.json', 'r') as file:
			data = json.load(file)
			return [Item(**item) for item in data]
	except FileNotFoundError:
		return []
	except Exception as e:
		print(f'Error: {e}')
		sys.exit()
#end load_item_prices

def save_item_prices(item_prices: list[Item]) -> None:
	# Delete the old item prices JSON file
	try:
		os.remove('./data/item_prices.json')
	except FileNotFoundError:
		pass

	# Sort the items by id before saving
	item_prices.sort(key=lambda x: x.id)

	# Save the item prices dictionary to the JSON file
	with open('./data/item_prices.json', 'w') as file:
		json.dump([item.to_dict() for item in item_prices], file, indent=4)
#end save_item_prices

def get_item_id(item_name: str, items_dict: dict) -> int:
	# File Structure: { "ItemId": { "en": "Item Name" }, ... }

	# Get the item ID from the items dictionary (the "en" property matching item)
	item_id = next((int(k) for k, v in items_dict.items() if v['en'] == item_name), None)
	return item_id
#end get_item_id

def get_item_name(item_id: int, items_dict: dict) -> str:
	# File Structure: { "ItemId": { "en": "Item Name" }, ... }

	# Get the item name from the items dictionary (the "en" property matching item)
	item_name = items_dict[str(item_id)]['en']
	return item_name
#end get_item_name

def get_local_item_price(item_id: int, item_prices: list[dict]) -> int:
	# Get the item from the item prices list if possible
	price_object: Item = next((x for x in item_prices if x.id == item_id), None)
	if (price_object != None):
		# Check if the timestamp is over 24 hours old
		if (int(time.time()) - price_object.timestamp <= 86400):
			return price_object.price
	
	# If the price isn't in the dictionary or old, return -1
	return -1
#end get_item_price

def get_item_prices(item_ids: list[int], item_prices: list[Item], items_dict: dict) -> dict:
	# Dictionary of item prices
	# Format: { "tem Id: Price }
	res_item_prices = {}
	
	# Get the prices for each item in the list
	# List of items that need to be looked up by the API
	needed_item_ids: list[int] = []
	for item_id in item_ids:
		price = get_local_item_price(item_id, item_prices)
		
		# If not in local storage, add to the list of items to look up
		if price == -1:
			needed_item_ids.append(item_id)
		else:
			res_item_prices[item_id] = price
	
	# Get the prices for the items from Universalis
	if len(needed_item_ids) > 0:
		print(f'Getting prices for {len(needed_item_ids)} items from Universalis...')
		api = UniversalisApi(DATA_CENTER)
		api_prices = api.get_item_prices(needed_item_ids)

		# Get the individual prices from the API response
		for i in range(len(needed_item_ids)):
			item_id = needed_item_ids[i]
			item_name = get_item_name(item_id, items_dict)
			api_price = int(api.get_item_price(item_id, api_prices))
			res_item_prices[item_id] = api_price

			# Save the new prices to the item prices dictionary
			item = Item(item_id, item_name, api_price)
			set_item_price(item, item_prices)

	# Return the dictionary of item prices
	return res_item_prices
#end get_item_prices

def set_item_price(new_item: Item, item_prices: list[dict]) -> None:
	# Set the item price in the item prices dictionary
	existing_item = next((x for x in item_prices if x.name == new_item.name), None)
	if existing_item:
		existing_item.price = new_item.price
		existing_item.timestamp = new_item.timestamp
	else:
		item_prices.append(new_item)
#end set_item_price

def main(home_file_name: str) -> None:
	local_items_dict = load_items_db()
	local_item_prices = load_item_prices()
	
	# Each '1' representing a thousand
	total: int = 0
	
	# Open the list.txt file and read each line
	item_lines = [] # Format: "Item Name: Quantity"
	try:
		with open(f'./homes/{home_file_name}', 'r') as file:
			# Loop through each line in the file
			for line in file:
				# Clean the line
				line = line.strip()
				item_lines.append(line)
	except FileNotFoundError:
		print(f'Error: File "{home_file_name}" not found.')

	# Loop through each line in chunks of 100 (max item limit for Universalis) API calls
	for i in range(0, len(item_lines), 100):
		# Get the item names and quantities from the line
		items = item_lines[i:i+100]
		item_names = [item.split(': ')[0] for item in items]
		item_ids = [get_item_id(item, local_items_dict) for item in item_names]
		item_quantities = [int(item.split(': ')[1]) for item in items]

		# Get the prices for each item (in the form of a dict of item ids and prices)
		item_prices = get_item_prices(item_ids, local_item_prices, local_items_dict)

		# Add the total for this chunk of items
		for j in range(len(item_ids)):
			item_id = item_ids[j]
			price = item_prices[item_id]
			quantity = item_quantities[j]
			total += price * quantity

	# Print the total
	print(f'\nApprox. Total: {int(total):,}')

	# Save the new price data
	save_item_prices(local_item_prices)
#end main


if __name__ == '__main__':
	home_file_name: str = ''

	# Get first argument (file name)
	if len(sys.argv) > 1:
		home_file_name = sys.argv[1]
	else:
		print('Error: No file name provided.')
		sys.exit()

	main(home_file_name)