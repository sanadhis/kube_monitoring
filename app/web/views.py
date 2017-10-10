from django.http import HttpResponse
from django.template import loader
from influxdb_metrics.utils import query

def index(request):
    queryDB  = "SELECT * FROM \"cpu/usage_rate\" WHERE namespace_name = 'default' ORDER BY time DESC LIMIT 100 "
    h2o_data = query(queryDB)
    template = loader.get_template('adminlte/base.html')
    result = [x for x in h2o_data.get_points()]    
    context = {
        'title' : "CPU Usage",
        'result': result,
    }
    return HttpResponse(template.render(context,request))
