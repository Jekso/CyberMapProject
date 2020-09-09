from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from elasticsearch import Elasticsearch
from Heisenberg.config import config
from Heisenberg.bootstrap import Scanner
import Heisenberg.Helpers.Logger as Logger
from datetime import datetime
from django.core.files.storage import default_storage
from django.conf import settings
import os


class StartScanView(APIView):
    permission_classes = (IsAuthenticated,)    
    parser_class = (FileUploadParser,) 

    def post(self, request):

        target_ips_file = None
        excluded_ips_file = None
        ip_range = None
        ports = None


        if 'target_ips_file' not in request.FILES and 'ip_range' not in request.data:
            return Response({'message': 'Please include ip file or a single ip or an ip range'})


        if 'target_ips_file' in request.FILES:
            file = request.FILES['target_ips_file']
            file_name = default_storage.save(file.name, file)
            target_ips_file = os.path.join(settings.MEDIA_ROOT, file_name)

        if 'excluded_ips_file' in request.FILES:
            file = request.FILES['excluded_ips_file']
            file_name = default_storage.save(file.name, file)
            excluded_ips_file = os.path.join(settings.MEDIA_ROOT, file_name)

        if 'ip_range' in request.data and 'target_ips_file' not in request.FILES:
            ip_range = request.data.get('ip_range')

        if 'ports' in request.data:
            ports = ','.join(request.data.getlist('ports'))
    
        scanner = Scanner(target_ips_file=target_ips_file, ip_range=ip_range, excluded_ips_file=excluded_ips_file, ports=ports)
        status = scanner.scan()

        if status:
            return Response({'message': 'scan is working on background...'})
        else:
            return Response({'message': 'error happen during process, check logs index.'})




class GetResultsView(APIView):
    permission_classes = (IsAuthenticated,)     

    def get(self, request):
        _es = Elasticsearch([{'host': config['elasticsearch']['host'],'port': config['elasticsearch']['port']}])
        from_i = request.data.get('from', 0)
        size = request.data.get('size', 50)
        ip = request.data.get('ip', None)
        ports = request.data.get('ports', None)
        services = request.data.get('services', None)

        if ip is not None:
            query = {'match': {'ip': ip}}
            op = f'searching for ip: {ip}'
        elif ports is not None:
            query = {'terms': {'port': ports}}
            op = f'searching for ports: {ports}'
        elif services is not None:
            query = {'terms': {'service_name': services}}
            op = f'searching for services: {services}'
        else:
            query = {'match_all': {}}
            op = f'get all data'


        body = {
            'from':from_i,
            'size':size,
            'query': query
        }

        res = _es.search(index=config['elasticsearch']['index'], body=body)

        Logger.search_log(op)

        content = {'operation': op, 'data': {'results_count': res['hits']['total']['value'], 'results': [x["_source"] for x in res['hits']['hits']]}, 'error': '', 'status_code': '200'}
        return Response(content)