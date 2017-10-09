from influxdb import InfluxDBClient
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from influxdb_metrics.utils import query
import json

def index(request):
    queryDB  = 'SELECT * from h2o_feet LIMIT 3'
    h2o_data = query(queryDB)
    result = [x for x in h2o_data.get_points()]
    return JsonResponse(result,safe=False)
    #return HttpResponse(result)
