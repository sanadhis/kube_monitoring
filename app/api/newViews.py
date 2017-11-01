from influxdb import InfluxDBClient
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
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
            content = {'please move along': 'nothing to see here'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'POST':
        body = request.body
        return HttpResponse(body)
