from influxdb import InfluxDBClient
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from influxdb_metrics.utils import query
from requests.exceptions import ConnectionError
from influxdb.exceptions import InfluxDBClientError
import json
import logging
import re

logger = logging.getLogger(__name__)

@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def index(request):
    if request.method == 'GET':
        path = request.path
        measurement = re.findall(r'^/api/(\S+)',path)[0]
        try:
            queryDB  = 'SELECT * from "' + measurement + '" LIMIT 10'
            gpu_data = query(queryDB)
            result = [x for x in gpu_data.get_points()]
            return JsonResponse(result,safe=False)
        except ConnectionError as e:
            message = {"code":500,"message":"Can't connect to influxdb"}
            return JsonResponse(message,status=500)
        except InfluxDBClientError as e:
            message = {"code":500,"message":"Wrong configuration to influxdb"}
            logger.error(e)
            return JsonResponse(message,status=500)
        
    elif request.method == 'POST':
        body = request.body
        return HttpResponse(body)