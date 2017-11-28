# Influxdb core
from influxdb               import InfluxDBClient
from influxdb_metrics.utils import query
from influxdb.exceptions    import InfluxDBClientError

# Django core
from django.core     import serializers
from django.http     import HttpResponse
from django.template import loader

# Rest framework core
from rest_framework.decorators import api_view, permission_classes
from rest_framework            import permissions

# Python native
from requests.exceptions import ConnectionError
import logging
import re
import os

logger = logging.getLogger(__name__)

## Custom user authentication for web
WEB_USERNAME = os.getenv("WEB_USERNAME", None)
WEB_PASSWORD = os.getenv("WEB_PASSWORD", None)

@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def index(request):
    try:
        path  = request.path
        table = re.findall(r'^/web/(\S+)',path)[0]
    except IndexError:
        response_message = {"code":404,"message":"Not found"}
        template = loader.get_template('adminlte/404.html')
        return HttpResponse(template.render({}, request))
    
    query_measurement    = "SHOW MEASUREMENTS"
    influxdb_measurement = query(query_measurement)
    measurements         = list(influxdb_measurement.get_points())

    # Set default request
    namespace = "default"
    limit     = "100"
    context = {
                'title' : "Kube Monitoring",
                'measurements' : measurements,
               }

    try:
        influx_query = 'SELECT * FROM "' + table + '" WHERE (namespace_name = \'' + namespace + '\') LIMIT ' + limit
        stats        = query(influx_query)
        result       = list(stats.get_points())
        title        = (table.replace("/"," ")).upper()
        template     = loader.get_template('adminlte/base.html')        
        
        context['title']  =  title
        context['result'] = result
        
        logger.info("Influxdb is working")
        return HttpResponse(template.render(context, request))
    except AttributeError as err:
        template = loader.get_template('adminlte/500.html')
        context['title']  =  "500"
        logger.error("Query Error: Check query to Influxdb")
        return HttpResponse(template.render(context, request),status=500)
    
    except ConnectionError as err:
        template = loader.get_template('adminlte/500.html')
        context['title']  =  "500"
        logger.error("Connection Error: Check connection to Influxdb")
        return HttpResponse(template.render(context, request),status=500)
