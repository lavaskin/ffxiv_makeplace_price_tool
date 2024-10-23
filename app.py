import sys
import os
from dotenv import load_dotenv

from src.item import Item
from src.universalis import UniversalisApi
from src.local import LocalData


def get_item_prices(item_ids: list[int], data_center: str, local_data: LocalData) -> dict:
	# Dictionary of item prices
	# Format: { "tem Id: Price }
	res_item_prices = {}
	
	# Get the prices for each item in the list
	# List of items that need to be looked up by the API
	needed_item_ids: list[int] = []
	for item_id in item_ids:
		price = local_data.get_local_item_price(item_id)
		
		# If not in local storage, add to the list of items to look up
		if price == -1:
			needed_item_ids.append(item_id)
		else:
			res_item_prices[item_id] = price
	
	print(f'Found {len(res_item_prices)} prices in local storage from the last 24hrs.')
	
	# Get the prices for the items from Universalis
	if len(needed_item_ids) > 0:
		print(f'Getting prices for {len(needed_item_ids)} items from Universalis...')
		api = UniversalisApi(data_center)
		
		# Get prices from the API for the needed items
		api_prices = api.get_item_prices(needed_item_ids)
		if api_prices != None:
			# Get the individual prices from the API response
			for i in range(len(needed_item_ids)):
				item_id = needed_item_ids[i]
				item_name = local_data.get_item_name(item_id)
				api_price = api.get_item_price(item_id, api_prices)
				if api_price == None:
					continue

				# Save the new prices to the item prices dictionary
				res_item_prices[item_id] = int(api_price)
				item = Item(item_id, item_name, int(api_price))
				local_data.set_item_price(item)

	# Return the dictionary of item prices
	return res_item_prices
#end get_item_prices

def read_home_file(file_name: str) -> list[str]:
	item_lines = []
	dye_mode = False

	try:
		with open(file_name, 'r') as file:
			for line in file:
				line = line.strip()

				# Stop when we get to the line denoting the start of the items with dye list
				if line == 'Furniture (With Dye)':
					break

				# Enable dye mode if we reach the dyes section (as it doesn't do the name of the dye by default)
				if line == 'Dyes':
					dye_mode = True
					continue

				# Skip empty, header lines and dividing lines
				if len(line) == 0 or line[0] == '=' or ': ' not in line:
					continue

				# If in dye mode, append " Dye" to the end of the name of the item (before the semi colon)
				if dye_mode:
					line = line.split(': ')
					line[0] += ' Dye'
					line = ': '.join(line)
				item_lines.append(line)
	except FileNotFoundError:
		print(f'Error: File "{file_name}" not found.')
		sys.exit(0)

	return item_lines
#end read_home_file

def main(home_file_name: str, data_center: str) -> None:
	local_data = LocalData()
	
	# Each '1' representing a thousand
	total: int = 0
	
	# Read the home file and return a list of item lines in the format "Item Name: Quantity"
	item_lines = read_home_file(home_file_name)
	print(f'Found {len(item_lines)} items in the list.')

	# Loop through each line in chunks of 100 (max item limit for Universalis) API calls
	for i in range(0, len(item_lines), 100):
		# Get the item names and quantities from the line
		items_chunk = item_lines[i:i+100]
		item_names = [item.split(': ')[0] for item in items_chunk]
		item_quantities = [int(item.split(': ')[1]) for item in items_chunk]
		item_ids = [local_data.get_item_id(name) for name in item_names]

		# Get the prices for each item (in the form of a dict of item ids and prices)
		item_prices = get_item_prices(item_ids, data_center, local_data)

		# Add the total for this chunk of items
		for j in range(len(item_ids)):
			item_id = item_ids[j]
			try:
				item_prices[item_id]
			except KeyError:
				print(f"Warn: Couldn't get price for {item_names[j]} (ID: {item_id})")
				continue
			price = item_prices[item_id]
			quantity = item_quantities[j]
			total += price * quantity

	# Print the total
	print(f'\nApproximate Total: {int(total):,} Gil')

	# Save the new price data
	local_data.save_item_prices()
#end main


# ARGUMENTS:
# 1: Home File Name (Excluding .list.txt)
# 2: Data Center (optional)
if __name__ == '__main__':
	home_file_name: str = ''
	data_center: str = 'Aether'

	# Get first argument (file name)
	if len(sys.argv) > 1:
		home_file_name = sys.argv[1]

		# Get second argument (data center)
		if len(sys.argv) > 2:
			data_center = sys.argv[2]
	else:
		print('Error: No file name provided.')
		sys.exit(0)

	# Process the home file name (remove file extensions) if they're included
	home_file_name = home_file_name.replace('.list', '')
	home_file_name = home_file_name.replace('.txt', '')

	# Load the .env file and create the path to the home file
	load_dotenv()
	makeplace_dir = os.getenv('MAKEPLACE_SAVES_PATH')
	if makeplace_dir:
		if not makeplace_dir.endswith('/'):
			makeplace_dir += '/'
		home_file_name = f'{makeplace_dir}{home_file_name}.list.txt'
	else:
		print('Error: MAKEPLACE_SAVES_PATH not found in .env file.')
		sys.exit(0)

	main(home_file_name, data_center)
#end __main__