class BaseScanner:
    """
    Base Scanner Class

    """

    def __init__(self, target_ips_file=None, ip_range=None, excluded_ips_file=None, ports=None):
        self.target_ips_file = target_ips_file
        self.ip_range = ip_range
        self.excluded_ips_file = excluded_ips_file
        self.ports = ports
        self.out = {}
        


    def scan(self):
        pass


    def handler(self):
        pass
