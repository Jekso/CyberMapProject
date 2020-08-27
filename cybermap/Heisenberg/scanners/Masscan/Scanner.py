import subprocess
import json
from datetime import datetime
from elasticsearch import Elasticsearch 
from Heisenberg.scanners.BaseScanner import BaseScanner
from Heisenberg.scanners.Masscan.config import config

class Scanner(BaseScanner):
    """
    Masscan Scanner Wrapper

    """
    def __init__(self, target_ips_file=None, ip_range=None, excluded_ips_file=None, ports='--top-ports'):
        BaseScanner.__init__(self, target_ips_file, ip_range, excluded_ips_file, ports)
        self.rate = config['rate']
        self.source_ip = config['source_ip']
        self.scanner_path = config['scanner_path']
        self.temp_file = config['scanner_path'] + '/temp.json'
        self.out = None



    def scan(self):
        command = f'{self.scanner_path}/masscan {self.ip_range} {self.ports} --rate {self.rate} --banners --source-ip {self.source_ip} -oJ {self.temp_file} > /dev/null 2>&1 && cat {self.temp_file} && rm -rf {self.temp_file}'
        res = subprocess.Popen([command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True).communicate()[0].decode('utf-8')
        self.out = json.loads(res)



    def transform(self):
        if self.out == None:
            return None
        hosts = {}
        for scan in self.out:
            ip = scan.get('ip')
            port = scan.get('ports')[0].get('port')
            service = scan.get('ports')[0].get('service')
            if ip not in hosts:
                hosts[ip] = {port: []}
                if service:
                    hosts[ip][port].append({'name': service.get('name'), 'banner': service.get('banner')})
            else:
                host = hosts.get(ip)
                if port not in host:
                    host[port] = []
                if service:
                    host[port].append({'name': service.get('name'), 'banner': service.get('banner')})
        self.out = {'tool': 'masscan', 'date': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'results': hosts}
        return hosts



    def commit(self):
        _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        
        if not _es.ping():
            return False
        
        res = _es.index(index='scans', doc_type='hosts', body=self.out)
        return res['result'] == 'created'



    def start_pipeline(self):
        self.scan()
        if self.transform() != None:
            return self.commit()
        return False
