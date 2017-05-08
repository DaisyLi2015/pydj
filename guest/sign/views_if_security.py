
# 实现接口签名代码

# user sign + timestrap
import hashlib
import time

from django.http import JsonResponse


def user_sgin(request):

    client_time = request.POST.get('time','')
    client_sign = request.POST.get('sign','')
    if client_time == '' or client_sign == '':
        return "sign null"

    # time of server
    now_time = time.time()
    server_time = str(now_time).split('.')[0]

    # get time
    time_difference = int(server_time)-int(client_time)
    if time_difference >=60:
        return "timeout"

    # sign check
    md5 = hashlib.md5()
    sign_str = client_time +"&Guest-Bugmaster"
    sign_bytes_utf8 = sign_str.encode(encoding='utf-8')
    md5.update(sign_bytes_utf8)
    server_sign = md5.hexdigest()
    if server_sign != client_sign:
        return "sign error"
    else:
        return "sign right"

# add event interface ---add sign+timestrap

def add_event(request):
    sign_result = user_sgin(request)
    if sign_result == "sign null":
        return JsonResponse({'status':10011,'message':'user sign null'})
    elif sign_result == "timeout":
        return  JsonResponse({'status':10012,'message':'user sign timeout'})
    elif sign_result == "sign error":
        return JsonResponse({'status':10013,'message':'user sign error'})