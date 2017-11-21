from influxdb import InfluxDBClient
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from influxdb_metrics.utils import query
from requests.exceptions import ConnectionError
import json

@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def index(request):
    if request.method == 'GET':
        try:
            queryDB  = 'SELECT * from h2o_feet LIMIT 3'
            h2o_data = query(queryDB)
            result = [x for x in h2o_data.get_points()]
            return JsonResponse(result,safe=False)
        except ConnectionError as e:
            message = {"code":500,"message":"Can't connect to influxdb"}
            return JsonResponse(message,status=500)
        
    elif request.method == 'POST':
        body = request.body
        return HttpResponse(body)
