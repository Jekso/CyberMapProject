from datetime import datetime
from elasticsearch import Elasticsearch
from Heisenberg.config import config



def scan_log(scanner):
    _es = Elasticsearch([{'host': config['elasticsearch']['host'],'port': config['elasticsearch']['port']}])
    log_index = {'type': 'info-scan', 'message': f"new scan using {scanner}", 'date': datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
    _es.index(index=config['elasticsearch']['logs_index'], doc_type='_doc', body=log_index)



def search_log(message):
    _es = Elasticsearch([{'host': config['elasticsearch']['host'],'port': config['elasticsearch']['port']}])
    log_index = {'type': 'info-search', 'message': message, 'date': datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
    _es.index(index=config['elasticsearch']['logs_index'], doc_type='_doc', body=log_index)



def error_log(message):
    _es = Elasticsearch([{'host': config['elasticsearch']['host'],'port': config['elasticsearch']['port']}])
    log_index = {'type': 'error', 'message': message, 'date': datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
    _es.index(index=config['elasticsearch']['logs_index'], doc_type='_doc', body=log_index)