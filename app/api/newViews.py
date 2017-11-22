from influxdb import InfluxDBClient
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from influxdb_metrics.utils import query
from requests.exceptions import ConnectionError
from influxdb.exceptions import InfluxDBClientError
from django.core import serializers
import json
import logging
import re

logger = logging.getLogger(__name__)

@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def index(request):
    path = request.path
    measurement = re.findall(r'^/api/(\S+)',path)[0]

    if request.method == 'GET':
        try:
            queryDB  = 'SELECT * from "' + measurement + '" LIMIT 10'
            logger.debug(queryDB)

            kube_data = query(queryDB)
            response_message = (list(kube_data.get_points()))
            status   = 200
        except ConnectionError as e:
            response_message = {"code":500,"message":"Can't connect to influxdb"}
            status   = 500            
        except InfluxDBClientError as e:
            response_message = {"code":500,"message":"Wrong configuration to influxdb"}
            logger.error(e)
            status   = 500            
            
    elif request.method == 'POST':
        body = json.loads(request.body.decode())
        try:
            namespace = body['namespace']
            limit     = body['limit']
            queryDB  = 'SELECT * FROM "' + measurement + '" WHERE (namespace_name = \'' + namespace + '\') LIMIT ' + limit
            logger.debug(queryDB)

            kube_data = query(queryDB)                        
            response_message = json.dumps(list(kube_data.get_points()))
            status   = 200
        except KeyError:
            response_message = {"code":500,"message":"Request body is not valid"}
            logger.error("Invalid request body")
            status   = 500  
        except ConnectionError as e:
            response_message = {"code":500,"message":"Can't connect to influxdb"}
            logger.error("Connection to influxdb server fails")            
            status   = 500            
        except InfluxDBClientError as e:
            response_message = {"code":500,"message":"Wrong configuration or query to influxdb"}
            logger.error(e)
            status   = 500  

    return JsonResponse(response_message, status=status, safe=False)
    