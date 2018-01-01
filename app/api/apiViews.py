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
import json
import logging
import re
import os

# Set application logging
logger = logging.getLogger(__name__)

# Custom authentication for API
# Obtain username and password for REST API service from environment
API_USERNAME = os.getenv("API_USERNAME")
API_PASSWORD = os.getenv("API_PASSWORD")

# Allow cross-site request forgery
@method_decorator(csrf_exempt, name='dispatch')
def index(request):
    """
    Main function to give response for http request.
    Filter non HTTP POST request.
    Args:
        request  (HttpRequest)  : User http request.
    Returns:
        response (JsonResponse) : Response of the request in JSON format.
    """

    # Ignore request aside from HTTP POST
    if not request.method == 'POST':
        logger.info("Attempt to perform non-POST request")
        response_message = {"code":400,"message":"Bad request"}
        status           = 400                     
        return JsonResponse(response_message, status=status, safe=False)

    # Give appropriate response for JSON        
    else:     
        return process_request(request)

def process_request(request):
    """
    Function to process http POST request.
    Give appropriate response for metrics query.
    Args:
        request  (HttpRequest)  : User http request.
    Returns:
        response (JsonResponse) : Response of the request in JSON format.
    """

    # get request credentials from request header
    username = request.META.get('HTTP_X_USERNAME')
    password = request.META.get('HTTP_X_PASSWORD')

    # clarify request redentials
    # case if request provides empty username and password
    if not username or not password:
        logger.info("Unauthorized request")            
        response_message = {"code":401,"message":"You are not authorized"}
        status           = 401

    # case if request credentials do not match setting in environment
    elif username != API_USERNAME or password != API_PASSWORD:
        logger.info("Unauthorized user")                        
        response_message = {"code":401,"message":"Username and password is not recognized"}
        status           = 401          

    # if credentials match  
    else:
        # attempt to find requested metrics
        try:
            path        = request.path
            # find using regex, e.g. `/api/cpu/usage_rate` => `cpu/usage_rate`
            measurement = re.findall(r'^/api/(\S+)',path)[0]
        except IndexError:
            # catch error and return not found response
            response_message = {"code":404,"message":"Request not found"}
            return JsonResponse(response_message, status=404, safe=False)

        # Set default request properties
        request_body        = {}        
        namespace           = "default"      # Namespace of pods in kubernetes (virtual cluster)
        limit               = "100"          # Limit of query
        metric_aggregation  = False          # should be either detail or general
        time_begin_interval = "now()-60m"    # by default is last 10 minutes of metrics in measurement
        time_end_interval   = "now()"
        
        # Get request body
        try:
            request_body = json.loads(request.body.decode())  
        except:
            logger.info("No request body provided")
        
        # Get pods namespace
        try:
            namespace = request_body['namespace']
        except KeyError:
            logger.info("Invalid request body, settings request namespace property as default")            

        # Get size of query limit
        try:
            limit = request_body['limit']
        except KeyError:
            logger.info("Invalid request body, settings request limit property as default")   

        # Get aggregation type
        try:
            metric_aggregation  = request_body['agg']
        except:
            logger.info("No aggregation requested")

        # Get time interval of desired queries
        try:
            time_begin_interval = "'" + request_body['timeBeginInterval'] + "'" 
            time_end_interval   = "'" + request_body['timeEndInterval']   + "'" 
        except:
            logger.info("No time interval requested")

        # Perform queries to influxdb based on request's properties
        try:
            # case if aggregation is not requested
            # perform query based on namespace, limit, and time
            if not metric_aggregation == "pod-per-namespace" and not metric_aggregation == "all-pod" and not metric_aggregation == "all-namespace":
                influx_query = 'SELECT * FROM "' + measurement \
                                + '" where namespace_name = \'' + namespace + '\'' \
                                + ' and time > ' + time_begin_interval \
                                + ' and time < ' + time_end_interval \
                                + ' ORDER BY time desc' \
                                + ' LIMIT ' + limit
                kube_data    = query(influx_query)
                data_points  = list(kube_data.get_points())

            # case if aggregation is requested
            else:
                # formulate query to see usage by each pod in a namespace
                if metric_aggregation == "pod-per-namespace":
                    influx_query   = 'SELECT sum(value) from "' + measurement \
                                      + '" where namespace_name = \'' + namespace + '\'' \
                                      + ' and time > ' + time_begin_interval \
                                      + ' and time < ' + time_end_interval \
                                      + ' group by namespace_name,pod_name'

                # formulate query to see usage by all pods
                elif metric_aggregation == "all-pod":
                    influx_query   = 'SELECT sum(value) from "' + measurement \
                                      + '" where namespace_name != \'kube-system\'' \
                                      + ' and time > ' + time_begin_interval \
                                      + ' and time < ' + time_end_interval \
                                      + ' group by pod_name'   

                # formulate query to see usage accumulated per namespace-based
                elif metric_aggregation == "all-namespace":
                    influx_query   = 'SELECT sum(value) from "' + measurement \
                                      + '" where namespace_name != \'kube-system\'' \
                                      + ' and time > ' + time_begin_interval \
                                      + ' and time < ' + time_end_interval \
                                      + ' group by namespace_name'                    

                # Execute query
                kube_data   = query(influx_query)

                # form list from query's results; keys (group by key) and datapoints
                keys        = list(kube_data.keys()) 
                data_points = list(kube_data.get_points())

                # update datapoints to include each correspond key
                for key, data_point in zip(keys,data_points):
                    for k in key[1:]:
                        # update dict
                        data_point.update(k)
            
            # SUCCESS = 200
            # form final response message
            response_message = data_points
            status           = 200

        # catch error if influxdb is unreachable
        except ConnectionError as e:
            logger.error("Connection to influxdb server fails")                        
            response_message = {"code":500,"message":"Can't connect to influxdb"}
            status           = 500
        # catch error if configuration of connection or query to influxdb does not work         
        except InfluxDBClientError as e:
            logger.error(e)            
            response_message = {"code":500,"message":"Wrong configuration or query to influxdb"}
            status           = 500  

    # give appropriate response message if status is 200 but message is empty
    if not response_message and status == 200:
        response_message = {"code":200,"message":"Query returns empty set"}

    return JsonResponse(response_message, status=status, safe=False)