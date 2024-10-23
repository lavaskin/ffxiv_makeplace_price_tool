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
	
	# Get the prices for the items from Universalis
	if len(needed_item_ids) > 0:
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
		print(f'\nError: File "{file_name}" not found.')
		sys.exit(1)

	return item_lines
#end read_home_file

def main(home_file_name: str, data_center: str, gil_cutoff: int) -> None:
	local_data = LocalData()
	
	# Each '1' representing a thousand
	total: int = 0
	
	# Read the home file and return a list of item lines in the format "Item Name: Quantity"
	item_lines = read_home_file(home_file_name)

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
			
			# Check if the item price was found
			try:
				item_prices[item_id]
			except KeyError:
				print(f"Warn: Couldn't get price for {item_names[j]} (ID: {item_id})")
				continue
			price = item_prices[item_id]

			# Check if it's higher than the cutoff
			if gil_cutoff > 0 and price > gil_cutoff:
				print(f' > {item_names[j]} (ID: {item_id}) exceeded the cutoff ({price:,} Gil)')
				continue

			# Add the price to the total
			quantity = item_quantities[j]
			total += price * quantity

	# Print the total
	print(f'\nApproximate Total: {int(total):,} Gil')

	# Save the new price data
	local_data.save_item_prices()
#end main

# For getting all the available houses to fetch item prices for in your MakePlace saves directory
def get_house_item_list_options(makeplace_dir: str) -> str:
	# Find all the files with the name *.list.txt in the given dir and print them out
	try:
		files = os.listdir(makeplace_dir)
		house_files = [file for file in files if file.endswith('.list.txt')]
		if len(house_files) == 0:
			print('\nNo house files found in the MakePlace saves directory.')
			sys.exit(1)
		print('\nAvailable House Files:')
		for file in house_files:
			print(f' > {file.replace(".list.txt", "")}')
	except FileNotFoundError:
		print(f'\nError: Directory "{makeplace_dir}" not found.')
		sys.exit(1)
#end get_house_item_list_options

# ARGUMENTS:
# 1: Home File Name (Excluding .list.txt)
# 2 or 3: Data Center (optional)
# 2 or 3: Gil Cutoff (optional)
def get_arguments(args: list[str]) -> tuple[str, str, int]:
	home_file_name = ''
	data_center = 'Aether'
	gil_cutoff = 0

	# Get first argument (file name or "list")
	if len(args) > 0:
		home_file_name = args[0]
	else:
		print('\nError: No file name provided.')
		sys.exit(1)

	# Get second argument (data center OR gil cutoff)
	if len(args) > 1:
		# If the second argument is a number, it's the gil cutoff
		if args[1].isdigit():
			gil_cutoff = int(args[1])
		else:
			data_center = args[1]	

	# Get third argument
	if len(args) > 2:
		# If the third argument is a number, it's the gil cutoff
		if args[2].isdigit():
			gil_cutoff = int(args[2])
		else:
			data_center = args[2]

	return home_file_name, data_center, gil_cutoff
#end get_arguments


if __name__ == '__main__':
	home_file_name, data_center, gil_cutoff = get_arguments(sys.argv[1:])

	# Load the .env file and create the path to the home file
	load_dotenv()
	makeplace_dir = os.getenv('MAKEPLACE_SAVES_PATH')
	if makeplace_dir:
		# Fix windows path slashes
		makeplace_dir = makeplace_dir.replace('\\', '/')

		# If the home_file_name is "list", show the available house lists
		# Also only run if other parameters are not included as there could potentially be a house named "list"
		if home_file_name == 'list' and len(sys.argv) == 2:
			get_house_item_list_options(makeplace_dir)
			sys.exit(0)

		if not makeplace_dir.endswith('/'):
			makeplace_dir += '/'

		# Process the home file name (remove file extensions) if they're included
		home_file_name = home_file_name.replace('.list', '')
		home_file_name = home_file_name.replace('.txt', '')
		home_file_name = f'{makeplace_dir}{home_file_name}.list.txt'
	else:
		print('\nError: MAKEPLACE_SAVES_PATH not found in .env file.')
		sys.exit(1)

	# Run the app
	main(home_file_name, data_center, gil_cutoff)
#end __main__
