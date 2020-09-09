from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from elasticsearch import Elasticsearch
from Heisenberg.config import config
from Heisenberg.bootstrap import Scanner
from datetime import datetime


class StartScanView(APIView):
    permission_classes = (IsAuthenticated,)     

    def post(self, request):
        scanner = Scanner(ip_range='185.176.40.0/24')
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

        log_index = {'type': 'info-search', 'message': op, 'date': datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
        _es.index(index=config['elasticsearch']['logs_index'], doc_type='_doc', body=log_index)

        content = {'operation': op, 'data': {'results_count': res['hits']['total']['value'], 'results': [x["_source"] for x in res['hits']['hits']]}, 'error': '', 'status_code': '200'}
        return Response(content)