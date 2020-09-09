import subprocess
import json
from datetime import datetime
from elasticsearch import Elasticsearch
from Heisenberg.HostScanners.BaseScanner import BaseScanner
from Heisenberg.config import config
import Heisenberg.Helpers.Logger as Logger
from datetime import datetime
import threading
import traceback


_es = Elasticsearch([{'host': config['elasticsearch']['host'], 'port': config['elasticsearch']['port']}])
que = queue.Queue()

class Scanner(BaseScanner):
    """
    Masscan Scanner Wrapper

    """
    def __init__(self, target_ips_file=None, ip_range=None, excluded_ips_file=None, ports='--top-ports'):
        BaseScanner.__init__(self, target_ips_file, ip_range, excluded_ips_file, ports)
        self.rate = config['scanner']['options']['rate']
        self.source_ip = config['scanner']['options']['source_ip']
        self.scanner_path = config['scanner']['options']['scanner_path']
        self.temp_file = config['scanner']['options']['scanner_path'] + '/temp.json'
        self.target_ips_file = target_ips_file
        self.ip_range = ip_range
        self.excluded_ips_file = excluded_ips_file
        self.ports = ports




    def handler(self):
        try:
            target = self.ip_range if self.ip_range is not None else f'-iL {self.target_ips_file}'
            exclude = f'‐‐excludefile {self.excluded_ips_file}' if self.excluded_ips_file is not None else ''
            ports = f'-p{self.ports}' if self.ports != '--top-ports' else self.ports
            command = f'sudo {self.scanner_path}/masscan {target} {exclude} {ports} --rate {self.rate} --banners --source-ip {self.source_ip} -oJ {self.temp_file} > /dev/null 2>&1 && cat {self.temp_file} && rm -rf {self.temp_file}'
            print(command)
            res = subprocess.Popen([command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True).communicate()[0].decode('utf-8')
            results = json.loads(res)
            datenow = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            job_body = {'target_ips_file': self.target_ips_file, 'ip_range': self.ip_range, 'excluded_ips_file': self.excluded_ips_file, 'ports': self.ports, 'datetime': datenow}
            job = _es.index(index=config['elasticsearch']['jobs_index'], doc_type='_doc', body=job_body)
            for result in results:
                if 'service' not in result['ports'][0]:
                    continue
                scan_index = {}
                scan_index['job_id'] = job['_id']
                scan_index['ip'] = result['ip']
                scan_index['port'] = result['ports'][0]['port']
                scan_index['service_name'] = result['ports'][0]['service']['name']
                scan_index['service_banner'] = result['ports'][0]['service']['banner'] 
                scan_index['datetime'] = datenow
                _es.index(index=config['elasticsearch']['scans_index'], doc_type='_doc', body=scan_index)
            Logger.scan_log("Masscan")
            return True
        except Exception:
            Logger.error_log(traceback.format_exc())
            return False



    def scan(self):
        t1 = threading.Thread(target=self.handler)
        t1.start()
