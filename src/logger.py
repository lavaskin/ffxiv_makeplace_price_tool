from termcolor import colored


def log_warn(message: str) -> None:
	print(colored(f" > Warning: {message}", 'yellow'))

def log_error(message: str, new_line: bool = True) -> None:
	if new_line: print()
	print(colored(f"Error: {message}", 'red'))

def log_info(message: str) -> None:
	print(f" > {message}")
