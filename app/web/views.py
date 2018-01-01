# Influxdb core
from influxdb_metrics.utils import query
from influxdb.exceptions    import InfluxDBClientError

# Django core
from django.http                    import HttpResponse
from django.template                import loader
from django.shortcuts               import redirect
from django.contrib.auth.decorators import login_required

# Rest framework core
from rest_framework.decorators import api_view, permission_classes
from rest_framework            import permissions

# Python native
from requests.exceptions import ConnectionError
import logging
import re

# Set application logging
logger = logging.getLogger(__name__)

@api_view(['GET', 'POST'])                      # Accepts only GET and POST
@permission_classes((permissions.AllowAny,))    # Accept all using Basic and Session Authentication
@login_required(login_url='/web/login/')        # Force login
def main(request):
    """
    Main function to process request.
    Give response and render the views based on user request.
    Args:
        request  (HttpRequest)  : User http request.
    Returns:
        response (HttpResponse) : HTTP Response for the request.
    """

    # Set default request property
    namespace = "all"       # Display all kubernetes namespaces
    limit     = "1000"      # Limit to 1000 datapoints only

    # metrics to be displayed on main left sidebar of the web
    # uncomment the rest to display all on main left sidebar of the web
    metrics = [
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
    
    # Units for main measurements/metrics on the web
    units     = {
                    "cpu/usage_rate" : "millicores",
                    "gpu/usage"      : "megabytes(MB)",
                    "memory/usage"   : "bytes(B)",
                    "uptime"         : "milliseconds",
                }

    # Set default page title, logout_url, and metrics option
    context = {
                'page_title' : "Kube Monitoring",
                'metrics'    : metrics,
                'logout_url' : "/web/authentication/signout",
              }

    # interpret the requested metric from URL
    try:
        path        = request.path
        # find using regex, e.g. `/web/stats/cpu/usage_rate` => `cpu/usage_rate`
        query_stats = re.findall(r'^/web/stats/(\S+)',path)[0]
        # try to infer requested namespace in path e.g. `/web/stats/cpu/usage_rate/test` => `cpu/usage_rate` & `/test`
        pattern     = re.findall(r'[^/]*/[^/]*',query_stats)
    except IndexError:
        # catch error and redirect to default index page
        return redirect('/web/stats/index')

    # Special case for "uptime", e.g `web/stats/uptime/test` => `uptime` & `test`
    if query_stats.startswith("uptime"):
        pattern = query_stats.split("/")
        try:
            # append "/" in the beginning of namespace, e.g `/test`
            pattern[1] = "/" + pattern[1]
        except IndexError:
            # ignore if namespace is empty
            pass

    try:
        # get the desired measurement/metric
        measurement = pattern[0]
    except IndexError:
        # flag default, as "index"
        measurement = "index"

    try:
        # infer namespace (if applicable)
        namespace = pattern[1][1:]
    except IndexError:
        # ignore if namespace is empty
        pass

    # if the requested metric is index, render the index page
    if measurement == "index":
        template = loader.get_template('adminlte/index.html')
        status   = 200                
    else:                
        try:
            # for namespace "all", exclude only datapoints without namespace
            if namespace == "all":
                namespace_query = "namespace_name != ''"
            # aside, simply filter by requested namespace
            else:
                namespace_query = "namespace_name = '" + namespace + "'"
            
            # formulate query to influxdb server
            influx_query = 'SELECT * FROM "' + measurement \
                            + '" where ' + namespace_query \
                            + ' ORDER BY time desc' \
                            + ' LIMIT ' + limit
            
            # Execute query
            kube_data    = query(influx_query)
            
            # form list from query results; datapoints
            datapoints   = list(kube_data.get_points())
            
            # get title for page based on measurement
            page_title   = (measurement.replace("/"," ")).upper()

            # get the base template to display datapoints
            template     = loader.get_template('adminlte/base.html')        
        
            # override default page_title
            context['page_title']  = page_title

            # add datapoints from influxdb query as result to web
            context['result'] = datapoints

            # attempt to add unit per measurement
            try:
                context['unit'] = "- " + units[measurement]
            except KeyError:
                # if unit cannot be found in units dict
                context['unit'] = ""
    
            # SUCCESS = 200
            status = 200            
            logger.info("Influxdb is working")

        # catch error if result from query cannot be processed
        except AttributeError as err:
            template              = loader.get_template('adminlte/500.html')
            context['page_title'] = "500"
            status                = 500
            logger.error("Query Error: Check query to Influxdb")
        # catch error if influxdb is unreachable
        except ConnectionError as err:
            template              = loader.get_template('adminlte/500.html')
            context['page_title'] = "500"
            status                = 500
            logger.error("Connection Error: Check connection to Influxdb")
        # catch error if configuration of connection or query to influxdb does not work         
        except InfluxDBClientError as e:
            template              = loader.get_template('adminlte/500.html')
            context['page_title'] = "500"
            status                = 500
            logger.error("Connection Error: Check connection to Influxdb")

    return HttpResponse(template.render(context, request),status=status)

def render_login(request):
    """
    Function to response request with login page.
    Args:
        request  (HttpRequest)  : User http request.
    Returns:
        response (HttpResponse) : HTTP Response for the request.
    """

    # do not render login page if user is authenticated
    if request.user.is_authenticated:
        return redirect('/web/stats/index')
    else:
        # load login page template
        template             = loader.get_template('adminlte/login.html')
        
        # set login path
        context              = {}
        context["form_path"] = "/web/authentication/signin"
        
        # Considered as 200 SUCCESSFUL
        status               = 200

        return HttpResponse(template.render(context, request),status=status)
