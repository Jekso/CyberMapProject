import importlib
from Heisenberg.config.config import config


# register your scanner
all_scanners = {
    'masscan': 'Heisenberg.scanners.Masscan.Scanner',
    'nmap': 'Heisenberg.scanners.Nmap.Scanner'
}


scanner_module = importlib.import_module(all_scanners[config['scanner']])
Scanner =  scanner_module.Scanner