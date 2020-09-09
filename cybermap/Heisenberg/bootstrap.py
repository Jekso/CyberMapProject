import importlib
from Heisenberg.config import config


scanner_module = importlib.import_module(config['all_scanners'][config['scanner']['name']])
Scanner =  scanner_module.Scanner