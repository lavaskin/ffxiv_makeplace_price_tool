import time


class Item:
	def __init__(self, id: int, name: str, price: int, timestamp: int = -1) -> None:
		self.id = id
		self.name = name
		self.price = price

		# Auto set the timestamp if not provided
		if timestamp != -1:
			self.timestamp = timestamp
		else:
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