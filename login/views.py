from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from .models import *
import random
from control.tasks import send_sms_code


###########################################################
# Login/Logout
###########################################################

# login html and login
def login_index(request):
    try: code = request.build_absolute_uri().split('?')[1]
    except: code = None

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)

            if user.account.districts == '0': return redirect("control_index")
            else: return redirect('control_students')            

        return redirect("/login/?error")

    context = {"code": code}

    return render(request, 'login/login.html', context)


# logout
@login_required(login_url='login_index')
def login_logout(request):
    auth.logout(request)
    return redirect('login_index')


###########################################################
# Reset password
###########################################################

# reset html
def login_reset(request):
    try: code = request.build_absolute_uri().split('?')[1]
    except: code = None

    context = {"code": code}

    return render(request, 'login/reset.html', context)


# send reset code
def login_reset_send_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        users = User.objects.all()

        
        for u in users:
            if data['phone'] == u.username:

                c = ""
                for i in range(6): c += random.choice('1234567890')

                r, created = Reset.objects.get_or_create(phone = data['phone'])
                r.code = c
                r.save()
                send_sms_code.send(r.phone, c)

        return JsonResponse({"status": 200}, safe = False)
    return JsonResponse({"status": 500}, safe = False)


# reset complete
def login_reset_complete(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        code = Reset.objects.filter(phone=data['phone']).last()

        if code.code == data['code']:
            u = User.objects.get(username=data['phone'])

            u.set_password(data['password'])
            u.save()

            return JsonResponse({"status": 200}, safe = False)
        return JsonResponse({"status": 404}, safe = False)
    return JsonResponse({"status": 500}, safe = False)
