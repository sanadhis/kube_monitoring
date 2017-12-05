# Influxdb core
from influxdb               import InfluxDBClient
from influxdb_metrics.utils import query
from influxdb.exceptions    import InfluxDBClientError

# Django core
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Python native
from requests.exceptions import ConnectionError
from json.decoder import JSONDecodeError
import json
import logging
import re
import os

logger = logging.getLogger(__name__)

## Custom user authentication for API
API_USERNAME = os.getenv("API_USERNAME")
API_PASSWORD = os.getenv("API_PASSWORD")

@method_decorator(csrf_exempt, name='dispatch')
def index(request):

    if request.method == 'GET':
        logger.info("Attempt to perform GET request")
        response_message = {"code":400,"message":"Bad request using GET"}
        status           = 400                     
            
    elif request.method == 'POST':                
        # get credentials
        username = request.META.get('HTTP_X_USERNAME')
        password = request.META.get('HTTP_X_PASSWORD')

        # Check Credentials
        if username is None or password is None:
            logger.info("Unauthorized request")            
            response_message = {"code":401,"message":"You are not authorized"}
            status           = 401
        elif username != API_USERNAME or password != API_PASSWORD:
            logger.info("Unauthorized user")                        
            response_message = {"code":401,"message":"Username and password is not recognized"}
            status           = 401            
        else:
            try:
                path        = request.path
                measurement = re.findall(r'^/api/(\S+)',path)[0]
            except IndexError:
                response_message = {"code":404,"message":"Request not found"}
                return JsonResponse(response_message, status=404, safe=False)

            # Set default request
            namespace = "default"
            limit     = "100"
            body = {}
            
            try:
                # Get request body
                body = json.loads(request.body.decode())  
            except JSONDecodeError:
                logger.info("No request body provided")
            
            try:
                namespace = body['namespace']
            except KeyError:
                logger.info("Invalid request body, settings request namespace property as default")            

            try:
                limit = body['limit']
            except KeyError:
                logger.info("Invalid request body, settings request limit property as default")   

            try:
                influx_query   = 'SELECT * FROM "' + measurement + '" where namespace_name = \'' + namespace + '\' ORDER BY time desc LIMIT ' + limit
                logger.info(influx_query)

                kube_data        = query(influx_query)                        
                response_message = list(kube_data.get_points())
                status           = 200
            except ConnectionError as e:
                logger.error("Connection to influxdb server fails")                        
                response_message = {"code":500,"message":"Can't connect to influxdb"}
                status           = 500            
            except InfluxDBClientError as e:
                logger.error(e)            
                response_message = {"code":500,"message":"Wrong configuration or query to influxdb"}
                status           = 500  

    return JsonResponse(response_message, status=status, safe=False)
    