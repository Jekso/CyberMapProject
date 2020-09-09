
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
            'source_ip': '192.168.43.35',
            'scanner_path': '/home/heisenberg/Desktop/masscan/bin',
        }
    },

	'elasticsearch':
    {
		'host': '192.168.43.30',
		'port': '9200',
		'index': 'scans'
	},

    'allowed_hosts': ['localhost']

}