import requests
import sys


class UniversalisApi:
	base_url: str = 'https://universalis.app/api/v2'
	
	def __init__(self, data_center: str):
		self.dc = data_center
	#end __init__

	# Given a list of item ids, returns a list of objects with pricing data
	def get_item_prices(self, item_ids: list) -> list:
		# Check if amount of id's between 1 and 100
		if (len(item_ids) < 1 or len(item_ids) > 100):
			return None
		
		# Convert the list of item ids to a comma-separated string
		item_list = ','.join(map(str, item_ids))
		
		# Get the item prices from Universalis
		url = f'aggregated/{self.dc}/{item_list}'
		res = self.__get__(url)

		# Return the list from the response (the results object)
		if 'results' not in res:
			print(f'Error fetching prices: {res}\nEndpoint: {url}')
			sys.exit(0)

		return res['results']
	#end get_item_prices

	# Given an item id and a list of price objects from get_item_prices, returns the price of the item
	# If the item is not found, returns -1
	def get_item_price(self, item_id: int, item_price_list: list) -> int:
		# Find the item in the list
		item = next((x for x in item_price_list if x['itemId'] == item_id), None)
		if (item == None):
			return -1

		# Check first if there's a price for the item in the dc item['nq']['averageSalePrice']['dc']['price']
		item_average_price: dict = item['nq']['averageSalePrice']
		if 'dc' in item_average_price:
			return item_average_price['dc']['price']
		
		# Check if there's a reigon price for the item
		if 'region' in item_average_price:
			return item_average_price['region']['price']
		
		# If no price is found, return -1
		return -1
	#end get_item_price

	def get_available_worlds(self) -> dict:
		# Get the available worlds from Universalis
		url = 'worlds'
		return self.__get__(url)
	#end get_available_worlds

	# Generic method to get data from Universalis
	def __get__(self, endpoint: str) -> dict:
		# Get the item prices from Universalis
		url = f"{self.base_url}/{endpoint}"
		response = requests.get(url)
		return response.json()
	#end __get__
#end Api
