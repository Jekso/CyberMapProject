from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from elasticsearch import Elasticsearch
from Heisenberg.config.config import config as main_cnfg
from Heisenberg.bootstrap import Scanner

class StartScanView(APIView):
    permission_classes = (IsAuthenticated,)     

    def post(self, request):
        scanner = Scanner(ip_range='185.176.40.0/24')
        scanner.start_pipeline()
        return Response({'success': 1})




class GetResultsView(APIView):
    permission_classes = (IsAuthenticated,)     

    def get(self, request):
        _es = Elasticsearch([{'host': main_cnfg['elasticsearch']['host'],'port': main_cnfg['elasticsearch']['port']}])
        from_i = request.data.get('from', 0)
        size = request.data.get('size', 20)
        ip = request.data.get('ip', None)
        ports = request.data.get('ports', None)
        services = request.data.get('services', None)

        if ip is not None:
            query = {'match': {'ip': ip}}
        elif ports is not None:
            query = {'terms': {'port': ports}}
        elif services is not None:
            query = {'terms': {'service_name': services}}
        else:
            query = {'match_all': {}}


        body = {
            'from':from_i,
            'size':size,
            'query': query
        }

        res = _es.search(index=main_cnfg['elasticsearch']['index'], body=body)

        content = {'data': {'results_count': res['hits']['total']['value'], 'results': [x["_source"] for x in res['hits']['hits']]}, 'error': '', 'status_code': '200'}
        return Response(content)