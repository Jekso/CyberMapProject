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



    def handler(self):
        try:
            command = f'sudo {self.scanner_path}/masscan {self.ip_range} {self.ports} --rate {self.rate} --banners --source-ip {self.source_ip} -oJ {self.temp_file} > /dev/null 2>&1 && cat {self.temp_file} && rm -rf {self.temp_file}'
            res = subprocess.Popen([command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True).communicate()[0].decode('utf-8')
            results = json.loads(res)
            datenow = datetime.fromtimestamp(int(result['timestamp'])).strftime("%d/%m/%Y %H:%M:%S")
            for result in results:
                if 'service' not in result['ports'][0]:
                    continue
                scan_index = {}
                scan_index['ip'] = result['ip']
                scan_index['port'] = result['ports'][0]['port']
                scan_index['service_name'] = result['ports'][0]['service']['name']
                scan_index['service_banner'] = result['ports'][0]['service']['banner'] 
                scan_index['datetime'] = datenow
                _es.index(index=config['elasticsearch']['index'], doc_type='_doc', body=scan_index)
            Logger.scan_log("Masscan")
            return True
        except Exception:
            Logger.error_log(traceback.format_exc())
            return False



    def scan(self):
        t1 = threading.Thread(target=self.handler)
        t1.start()
        result = t1.join()
        return result
