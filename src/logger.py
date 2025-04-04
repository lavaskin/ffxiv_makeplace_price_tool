import platform

from termcolor import colored


is_windows = platform.system() == 'Windows'


def log_warn(message: str) -> None:
	if is_windows:
		print(f" > WARN: {message}")
	else:
		# Print the warning in yellow
		print(colored(f" > WARN: {message}", 'yellow'))

def log_error(message: str, new_line: bool = True) -> None:
	if new_line: print()
	if is_windows:
		print(f"ERR: {message}")
	else:
		# Print the error in red
		print(colored(f"ERR: {message}", 'red'))

def log_info(message: str) -> None:
	print(f" > {message}")
