from django.http import HttpResponse
from django.template import loader
from influxdb_metrics.utils import query
from requests.exceptions import ConnectionError
import logging

logger = logging.getLogger(__name__)

def index(request):
    try:
        queryDB  = "SELECT * FROM \"cpu/usage_rate\" WHERE (namespace_name = 'default' or namespace_name='vlsc' or namespace_name='dcsl') ORDER BY time DESC LIMIT 100 "
        h2o_data = query(queryDB)
        template = loader.get_template('adminlte/base.html')
        result = [x for x in h2o_data.get_points()]
        context = {
            'title' : "CPU Usage",
            'result': result,
        }
        logger.info("Influxdb is working")
        return HttpResponse(template.render(context, request))
    
    except ConnectionError as err:
        template = loader.get_template('web/500.html')
        context  = {}
        logger.error("Connection Error: Check connection to Influxdb")
        return HttpResponse(template.render(context, request),status=500)
