from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def index(request):
    return render(request,'index.html')

def Login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user) #login
            request.session['user'] = username  # record seesion info on browser
            response =  HttpResponseRedirect('/event_manage/')
            return response
            # return render(request,'event_managel.html')
        else:
            return render(request,'index.html',{'error':'username or password error!'})

# 发布会管理
# @ login_required
def event_manage(request):
    event_list = Event.objects.all()
    username = request.session.get('user','') #    reed seesion from browser
    return render(request,'event_manage.html',{"user":username,"events":event_list})

# 发布会名称搜索框
# @ login_required
def search_name(request):
    event_name = request.GET.get("name",'')
    event_list = Event.objects.filter(name__contains= event_name)
    return  render(request,"event_manage.html",{ "events": event_list})

# 嘉宾管理
# @login_required
def guest_manage(request):
    username = request.session.get("user", "")
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list,2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        #  if page is not an integer,deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # if page is out of range (e.g.9999),deliver last page of results.
        contacts = paginator.page(page.num_pages)
    return render(request,'guest_manage.html',{"user":username,"guests":contacts})

# 嘉宾名称搜索框
# @ login_required
def search_realname(request):
    guest_realname = request.GET.get("realname",'')
    guest_list = Guest.objects.filter(realname__contains= guest_realname)
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        #  if page is not an integer,deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # if page is out of range (e.g.9999),deliver last page of results.
        contacts = paginator.page(page.num_pages)
    return  render(request,"guest_manage.html",{ "guests": contacts})

# 嘉宾签到页面
# @login_required
def sign_index(request,event_id):
    event = get_object_or_404(Event,id=event_id)
    return render(request,'sign_index.html',{"event":event})

# 嘉宾签到
# @login_required
def sign_index_action(request,event_id):
    event = get_object_or_404(Event, id=event_id)
    phone = request.POST.get("phone","")

    result = Guest.objects.filter(phone = phone)
    if not result:
        return render(request,"sign_index.html",{"event":event,"hint":"phone error."})

    result = Guest.objects.filter(phone = phone,event_id = event_id)
    if not result:
        return render(request,"sign_index.html",{"event":event,"hint":"event id or phone error."})

    result = Guest.objects.get(phone =phone ,event_id=event_id)
    if result.sign:
        return render(request,"sign_index.html",{'event':event,'hint':"user has sign in."})

    else:
        Guest.objects.filter(phone=phone, event_id=event_id).update(sign ='1')
        return render(request,'sign_index.html',{'event':event,'hint':'sign in success!','guest':result})

# logout
@login_required
def logout(request):
    auth.logout(request) #logout
    response = HttpResponseRedirect('/index/')
    return response
