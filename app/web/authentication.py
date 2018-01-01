# Django core
from django.contrib.auth import authenticate, login, logout
from django.shortcuts    import redirect

# Python native
import logging

# Set application logging
logger = logging.getLogger(__name__)

# Custom decorator
def verify_request(func):
    """
    Decorator method for signin and signout function.
    Check HTTP request method.
    Signin and signout MUST BE performed by HTTP POST.
    Args:
        func  (function)  : method signin or signout.
    """

    def check_request(request):
        """
        Function to filter HTTP request.
        Args:
            request  (HttpRequest)  : http request.
        Returns:
            redirect : HTTP redirect (301)
        """

        if not request.method == 'POST':
            # redirect to login url if http method is not POST
            return redirect('/web/login/')
        # if POST
        else:
            # proceed the original function without modifying the request
            return func(request)
        
    return check_request

@verify_request     # Filter HTTP request, accept only HTTP POST
def signin(request):
    """
    Function to authenticate sign in request.
    Authenticate user and login request
    Args:
        request  (HttpRequest)  : User http request.
    Returns:
        redirect (redirect)     : HTTP redirect (301)
    """

    # Get username and password from HTTP POST request
    username = request.POST['username']
    password = request.POST['password']

    # Authenticate given username and password
    user     = authenticate(request, username=username, password=password)
    
    # Check if matched user can be found or not
    if user is not None:
        # login request session and user
        login(request, user)
        logger.info("Login Successfull")
        return redirect('/web/stats/index')
    else:
        # redirect to login page if user is not found
        logger.info("Login Failed")
        return redirect('/web/login/')

@verify_request     # Filter HTTP request, accept only HTTP POST
def signout(request):
    """
    Function to logout user and request
    Args:
        request  (HttpRequest)  : User http request.
    Returns:
        redirect (redirect)     : HTTP redirect (301)
    """

    # logout request session and user
    logout(request)
    logger.info("Logout Successfull")
    return redirect('/web/login/')
