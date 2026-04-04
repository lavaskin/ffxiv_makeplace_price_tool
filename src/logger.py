import platform
from termcolor import colored

IS_WINDOWS = platform.system() == 'Windows'

def log_warn(message: str) -> None:
	if IS_WINDOWS:
		print(f" > WARN: {message}")
	else:
		# Print the warning in yellow
		print(colored(f" > WARN: {message}", 'yellow'))
#end log_warn

def log_error(message: str, new_line: bool = True) -> None:
	if new_line: print()
	
	if IS_WINDOWS:
		print(f"ERR: {message}")
	else:
		# Print the error in red
		print(colored(f"ERR: {message}", 'red'))
#end log_error

def log_info(message: str) -> None:
	print(f" > {message}")
#end log_info
