from django.http import HttpResponse
from django.template import loader
from influxdb_metrics.utils import query

def index(request):
    queryDB  = 'SELECT * from h2o_feet LIMIT 3'
    h2o_data = query(queryDB)
    template = loader.get_template('adminlte/base.html')
    result = [x for x in h2o_data.get_points()]    
    context = {
        'result': result,
    }
    return HttpResponse(template.render(context,request))
