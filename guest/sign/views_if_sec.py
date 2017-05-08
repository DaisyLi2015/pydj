import base64

from django.contrib import auth as django_auth
import hashlib

from django.http import JsonResponse


# user auth
def user_auth(request):

    get_http_auth = request.META.get('HTTP_AUTHORIZATION',b'')
    auth = get_http_auth.split()
    try:
        auth_parts = base64.b64decode(auth[1].decode('iso-8859-1')\
                                     .partition(':'))

    except IndexError:
        return "null"

    userid,passwrod = auth_parts[0],auth_parts[2]
    user = django_auth.authenticate(username=userid,passwrod=passwrod)
    if user is not None and user.is_active:
        django_auth.login(request,user)
        return "success"
    else:
        return "fail"

# event search interface --add user auth
def get_event_list(request):
    auth_result = user_auth(request) #调用认证函数
    if auth_result == "null":
        return JsonResponse({'status':10011,'message':'user auth null'})

    if auth_result == 'fail':
        return JsonResponse({'status':10012,'message':'user auth fail'})

    eid = request.GET.get('eid'," ") # id of event
    name = request.GET.get('name'," ") # name of event

