
config = {

    
    'all_scanners':
    {
        'masscan': 'Heisenberg.HostScanners.Masscan.Scanner',
        'nmap': 'Heisenberg.HostScanners.Nmap.Scanner'
    },


	'scanner':
    {
        'name': 'masscan',
        'options':
        {
            'rate': '1000',
            'source_ip': '127.20.0.1',
            'scanner_path': '/home/heisenberg/Desktop/masscan/bin',
        }
    },

	'elasticsearch':
    {
		'host': 'localhost',
		'port': '9200',
		'index': 'scans',
        'logs_index': 'logs'
	},

    'allowed_hosts': ['localhost']

}