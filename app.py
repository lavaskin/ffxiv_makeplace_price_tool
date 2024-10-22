import sys
import json
import time
import os


# World Data: https://github.com/xivapi/ffxiv-datamining/blob/master/csv/World.csv
# #   InternalName	Name	    Region  UserType  DataCenter  IsPublic
# 99  Sargatanas	Sargatanas	1	    4	      4	          True
WORLD_INTERNAL_NAME = 'Sargatanas'
WORLD_REGION = 1
WORLD_DATA_CENTER = 4


class Item:
	def __init__(self, name: str, price: int, id: int):
		self.id = id
		self.name = name
		self.price = price
		self.timestamp = int(time.time()) # Set the timestamp to the current time
	#end __init__

	def to_dict(self) -> dict:
		return {
			'id': self.id,
			'name': self.name,
			'price': self.price,
			'timestamp': self.timestamp
		}
	#end to_dict
#end Item


def load_items_db() -> dict:
	# File Structure: { "ItemId": { "en": "Item Name" }, ... }

	# Load in the raw items databse JSON
	items_dict = {}
	with open('./items_db.json', 'r', encoding='utf-8') as file:
		items_dict = json.load(file)
	return items_dict
#end load_items_db

def load_item_prices() -> list:
	# Try to load in the raw item prices JSON
	# If it fails, return an empty dictionary
	try:
		with open('./data/item_prices.json', 'r') as file:
			data = json.load(file)
			return [Item(**item) for item in data]
	except:
		return []
#end load_item_prices

def save_item_prices(item_prices: list) -> None:
	# Delete the old item prices JSON file
	try:
		os.remove('./data/item_prices.json')
	except:
		pass

	# Save the item prices dictionary to the JSON file
	with open('./data/item_prices.json', 'w') as file:
		json.dump([item.to_dict() for item in item_prices], file)
#end save_item_prices

# Looks up the current price of an item on Universalis
# The API has a rate limit of 24 reqs/sec
def get_item_price_universalis(item_name: str, item_id: int, item_prices: list) -> int:
	# Sleep for 0.05 seconds to avoid rate limiting
	time.sleep(0.05)
	
	# Call API to get the item price
	price = 0 # Placeholder for now

	# ...

	# Add the item to the item prices dictionary
	new_item = Item(item_name, price, item_id)
	set_item_price(new_item, item_prices)

	return price
#end get_item_price_universalis

def get_item_id(item: str, items_dict: dict) -> int:
	# File Structure: { "ItemId": { "en": "Item Name" }, ... }

	# Get the item ID from the items dictionary (the "en" property matching item)
	item_id = next((int(k) for k, v in items_dict.items() if v['en'] == item), None)
	return item_id
#end get_item_id

def get_item_price(item: str, item_prices: list, items_dict: dict) -> int:
	# Get the item from the item prices list if possible
	price_object = next((x for x in item_prices if x.name == item), None)
	if (price_object != None):
		# Check if the timestamp is over 24 hours old
		if (int(time.time()) - price_object['timestamp'] <= 86400):
			return price_object.price
	
	# If the price isn't in the dictionary or old, get the price from Universalis
	item_id = get_item_id(item, items_dict)
	price = get_item_price_universalis(item, item_id, item_prices)

	return price
#end get_item_price

def set_item_price(new_item: Item, item_prices: list) -> None:
	# Set the item price in the item prices dictionary
	existing_item = next((x for x in item_prices if x.name == new_item.name), None)
	if existing_item:
		existing_item.price = new_item.price
		existing_item.timestamp = new_item.timestamp
	else:
		item_prices.append(new_item)
#end set_item_price

def main(file_name: str) -> None:
	items_dict = load_items_db()
	item_prices = load_item_prices()
	
	# Each '1' representing a thousand
	total: int = 0
	
	# Open the list.txt file
	with open(f'./homes/{file_name}.txt', 'r') as file:
		# Loop through each line in the file
		for line in file:
			# Clean the line
			line = line.strip()

			# Get the item name and quantity (Name: Quantity)
			item_name, quantity = line.split(': ')
			quantity = int(quantity)
			price = get_item_price(item_name, item_prices, items_dict)

			# Add the price to the total
			total += price * quantity

	# Print the total
	print(f'Approx. Total: {total * 1000:,}')

	# Save the new price data
	save_item_prices(item_prices)
#end main


if __name__ == '__main__':
	# Get first argument (file name)
	if len(sys.argv) > 1:
		file_name = sys.argv[1]

	main(file_name)