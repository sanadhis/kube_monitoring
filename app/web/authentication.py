from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
import logging

logger = logging.getLogger(__name__)

# Custom decorator
def verify_request(func):
    def check_request(request):
        if request.method == 'GET':
            return redirect('/web/login')
        elif request.method == 'POST':
            return func(request)
    return check_request

@verify_request
def signin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        logger.info("Login Successfull")
        return redirect('/web/stats/index')
    else:
        logger.info("Login Failed")
        return redirect('/web/login')

@verify_request
def signout(request):
    logout(request)