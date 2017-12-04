# Influxdb core
from influxdb               import InfluxDBClient
from influxdb_metrics.utils import query
from influxdb.exceptions    import InfluxDBClientError

# Django core
from django.core      import serializers
from django.http      import HttpResponse
from django.template  import loader
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

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
WEB_USERNAME = os.getenv("WEB_USERNAME")
WEB_PASSWORD = os.getenv("WEB_PASSWORD")

@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
@login_required(login_url='/web/login/')
def index(request):

    measurements = []
    context = {
                'measurements' : measurements
               }

    try:
        path  = request.path
        table = re.findall(r'^/web/stats/(\S+)',path)[0]
    except IndexError:
        return redirect('/web/stats/index')

    try:
        query_measurement    = "SHOW MEASUREMENTS"
        influxdb_measurement = query(query_measurement)
        measurements         = list(influxdb_measurement.get_points())
    except ConnectionError:
        template = loader.get_template('adminlte/500.html')
        context['title']  =  "500"
        status = 500
        logger.error("Connection Error: Check connection to Influxdb")

    # Set default request
    namespace = "default"
    limit     = "100"
    context = {
                'title' : "Kube Monitoring",
                'measurements' : measurements,
               }

    if table == "index":
        template = loader.get_template('adminlte/index.html')
        status   = 200                
    else:                
        try:
            influx_query = 'SELECT * FROM "' + table + '" WHERE (namespace_name = \'' + namespace + '\') LIMIT ' + limit
            stats        = query(influx_query)
            result       = list(stats.get_points())
            title        = (table.replace("/"," ")).upper()
            template     = loader.get_template('adminlte/base.html')        
            
            context['title']  =  title
            context['result'] = result
            
            status = 200            
            logger.info("Influxdb is working")
        except AttributeError as err:
            template = loader.get_template('adminlte/500.html')
            context['title']  =  "500"
            status = 500
            logger.error("Query Error: Check query to Influxdb")
        except ConnectionError as err:
            template = loader.get_template('adminlte/500.html')
            context['title']  =  "500"
            status = 500
            logger.error("Connection Error: Check connection to Influxdb")

    return HttpResponse(template.render(context, request),status=status)

def render_login(request):
    template = loader.get_template('adminlte/login.html')
    context  = {}
    context["form_path"] = "/web/authentication/signin"
    status   = 200     
    return HttpResponse(template.render(context, request),status=status)
