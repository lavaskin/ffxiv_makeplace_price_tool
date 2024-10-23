from src.item import Item
import json
import sys
import time
import os


class LocalData:
	item_prices_file_name: str = './data/item_prices.json'
	item_data_file_name: str = './data/items_db.json'
	item_data: dict = None
	item_prices: list[Item] = None
	
	def __init__(self):
		# Load in inital data for properties
		self.item_data = self.__load_items_db__()
		self.item_prices = self.__load_item_prices__()
	#end __init__

	def get_local_item_price(self, item_id: int) -> int:
		# Get the item from the item prices list if possible
		price_object: Item = next((x for x in self.item_prices if x.id == item_id), None)
		if (price_object != None):
			# Check if the timestamp is over 24 hours old
			if (int(time.time()) - price_object.timestamp <= 86400):
				return price_object.price
		
		# If the price isn't in the dictionary or old, return -1
		return -1
	#end get_item_price

	def set_item_price(self, new_item: Item) -> None:
		# Set the item price in the item prices dictionary
		existing_item = next((x for x in self.item_prices if x.name == new_item.name), None)
		if existing_item:
			existing_item.price = new_item.price
			existing_item.timestamp = new_item.timestamp
		else:
			self.item_prices.append(new_item)
	#end set_item_price

	def get_item_id(self, item_name: str) -> int:
		# Get the item ID from the items dictionary (the "en" property matching item)
		item_id = next((int(k) for k, v in self.item_data.items() if v['en'] == item_name), None)
		return item_id
	#end get_item_id

	def get_item_name(self, item_id: int) -> str:
		# File Structure: { "ItemId": { "en": "Item Name" }, ... }

		# Get the item name from the items dictionary (the "en" property matching item)
		item_name = self.item_data[str(item_id)]['en']
		return item_name
	#end get_item_name

	def save_item_prices(self) -> None:
		# Delete the old item prices JSON file
		try:
			os.remove(self.item_prices_file_name)
		except FileNotFoundError:
			pass

		# Sort the items by id before saving
		self.item_prices.sort(key=lambda x: x.id)

		# Save the item prices dictionary to the JSON file
		with open(self.item_prices_file_name, 'w') as file:
			json.dump([item.to_dict() for item in self.item_prices], file, indent=4)
	#end save_item_prices

	def __load_items_db__(self) -> dict:
		# Load in the raw items databse JSON
		items_dict = {}
		with open(self.item_data_file_name, 'r', encoding='utf-8') as file:
			items_dict = json.load(file)
		return items_dict
	#end load_items_db

	def __load_item_prices__(self) -> list[Item]:
		# Try to load in the raw item prices JSON
		# If it fails, return an empty dictionary
		try:
			with open(self.item_prices_file_name, 'r') as file:
				data = json.load(file)
				return [Item(**item) for item in data]
		except FileNotFoundError:
			return []
		except Exception as e:
			print(f'\nError: {e}')
			sys.exit(1)
	#end load_item_prices
#end LocalData