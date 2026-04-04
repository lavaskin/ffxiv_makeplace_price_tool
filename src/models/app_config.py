from dotenv import load_dotenv
import os
import sys

from src.logger import *

class AppConfig:
	def __init__(self, load_env: bool = True) -> None:
		# Define properties
		self.saves_path: str = ''
		self.outputEnabled: bool = False
		self.output_path: str = ''

		if load_env:
			self.load_env()
	#end __init__

	def load_env(self) -> None:
		load_dotenv() # Load environment variables from .env file

		self.saves_path = self.__get_env_variable__('MAKEPLACE_SAVES_PATH')
		self.saves_path = self.saves_path.replace('\\', '/') # Fix windows path slashes

		self.outputEnabled = self.__get_env_variable__('ENABLE_OUTPUT', default='false').lower() == 'true'
		self.output_path = self.__get_env_variable__('OUTPUT_PATH', default='./output')
	#end load_env

	def __get_env_variable__(self, key: str, default: str = '') -> str:
		value = os.getenv(key, default)
		if value == '':
			log_error(f'Environment variable "{key}" is not set and no default value provided.')
			sys.exit(1)
		return value
	#end get_env_variable
