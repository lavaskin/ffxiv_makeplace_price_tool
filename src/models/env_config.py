from dotenv import load_dotenv
import os
import sys

from src.logger import *

class EnvConfig:
	def __init__(self) -> None:
		load_dotenv() # Load environment variables from .env file

		self.saves_path = self.get_env_variable('MAKEPLACE_SAVES_PATH')
		self.saves_path = self.saves_path.replace('\\', '/') # Fix windows path slashes

		self.outputEnabled = self.get_env_variable('ENABLE_OUTPUT', default='false').lower() == 'true'
		self.output_path = self.get_env_variable('OUTPUT_PATH', default='./output')
	#end __init__

	def get_env_variable(self, key: str, default: str = '') -> str:
		value = os.getenv(key, default)
		if value == '':
			log_error(f'Environment variable "{key}" is not set and no default value provided.')
			sys.exit(1)
		return value
	#end get_env_variable
