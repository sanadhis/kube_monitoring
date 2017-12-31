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

@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
@login_required(login_url='/web/login/')
def index(request):

    try:
        path  = request.path
        table = re.findall(r'^/web/stats/(\S+)',path)[0]
    except IndexError:
        return redirect('/web/stats/index')

    # Set default request
    namespace = "default"
    limit     = "1000"

    measurements = [
                # "cpu/node_capacity",
                # "cpu/usage",
                "cpu/usage_rate",
                "gpu/usage",
                # "memory/node_capacity",
                "memory/usage",
                # "memory/cache",
                # "memory/rss",
                # "network/rx",
                # "network/rx_rate",
                # "network/tx",
                # "network/tx_rate",
                "uptime",
                ]

    units     = {
                    "cpu/usage_rate":"millicores",
                    "gpu/usage":"megabytes(MB)",
                    "memory/usage":"bytes(B)",
                    "uptime":"milliseconds",
                }

    context = {
                'title'        : "Kube Monitoring",
                'measurements' : measurements,
                'logout_url'   : "/web/authentication/signout",
               }

    if table == "index":
        template = loader.get_template('adminlte/index.html')
        status   = 200                
    else:                
        try:
            influx_query = 'SELECT * FROM "' + table + '" where namespace_name != \'\' ORDER BY time desc LIMIT ' + limit
            stats        = query(influx_query)
            result       = list(stats.get_points())
            title        = (table.replace("/"," ")).upper()
            template     = loader.get_template('adminlte/base.html')        
        
            context['title']  =  title
            context['result'] = result
            
            try:
                context['unit'] = "- " + units[table]
            except KeyError:
                context['unit'] = ""

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
    if request.user.is_authenticated:
        return redirect('/web/stats/index')
    else:
        template = loader.get_template('adminlte/login.html')
        context  = {}
        context["form_path"] = "/web/authentication/signin"
        status   = 200     
        return HttpResponse(template.render(context, request),status=status)
