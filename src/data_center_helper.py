from src.models.data_center import DataCenter
from src.logger import *

DATA_CENTERS = [
	# NA
	DataCenter('Aether', ['Adamantoise', 'Cactuar', 'Faerie', 'Gilgamesh', 'Jenova', 'Midgardsormr', 'Sargatanas', 'Siren']),
	DataCenter('Crystal', ['Balmung', 'Brynhildr', 'Coeurl', 'Diabolos', 'Goblin', 'Malboro', 'Mateus', 'Zalera']),
	DataCenter('Primal', []),
	DataCenter('Dynamis', []),

	# EU
	DataCenter('Chaos', []),
	DataCenter('Light', []),

	# Japan
	DataCenter('Elemental', ['Aegis', 'Atomos', 'Carbuncle', 'Garuda', 'Gungnir', 'Kujata', 'Tonberry', 'Typhon',]),
	DataCenter('Gaia', []),
	DataCenter('Mana', []),
	DataCenter('Meteor', []),

	# Oceania
	DataCenter('Materia', []),
]

# Checks if a given world arg is valid, aka:
# - If it's just a data center, check if it's valid
# - If it's both a dc and world (in the format "DC/World"), check if both are valid and the world is in the dc
def is_valid_dc_arg(arg: str):
	# Check if the arg is in the format "DC/World"
	if '/' in arg:
		dc_name, world_name = arg.split('/')
		if not is_valid_data_center(dc_name):
			return False
		return is_valid_world(world_name)
	else:
		return is_valid_data_center(arg)
#end is_valid_dc_arg

# Make sure the given data center exists
def is_valid_data_center(dc_name: str):
	for dc in DATA_CENTERS:
		if dc.name.lower() == dc_name.lower():
			return True
	log_error(f'Data center "{dc_name}" is not valid.')
	return False
#end is_valid_data_center

# Make sure the given world exists in any data center
def is_valid_world(world_name: str):
	for dc in DATA_CENTERS:
		for world in dc.worlds:
			if world.lower() == world_name.lower():
				return True
	log_error(f'World "{world_name}" is not valid.')
	return False
#end is_valid_world
