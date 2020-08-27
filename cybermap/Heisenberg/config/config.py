
config = {
	

	# -------------------------------------------------- Scanners Config START ---------------------------------------------------------------- #



	# scanner tool, valid options ['masscan', 'nmap']
	'scanner': 'masscan',



	# -------------------------------------------------- Scanners Config END ---------------------------------------------------------------- #







	# -------------------------------------------------- Elasticsearch Config START ---------------------------------------------------------------- #



	'elasticsearch': {


		# elasticsearch host
		'host': 'localhost',



		# elasticsearch port
		'port': '9200',



		# elasticsearch index name
		'index': 'scans'
	},




	# -------------------------------------------------- Elasticsearch Config END ---------------------------------------------------------------- #

}