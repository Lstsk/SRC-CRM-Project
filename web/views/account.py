from django.shortcuts import render, HttpResponse, redirect
from rbac import models
from rbac.service.init_permission import init_permission
from web.forms_web.registerform import UserRegisterForm
from django.contrib.auth import login,logout
from rbac.models import UserInfo

def Login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    user = request.POST.get('user')
    password = request.POST.get('password')
    request.session['username'] = user
    user_obj = models.UserInfo.objects.filter(name=user, password=password).first()
    if not user_obj:
        return render(request, 'login.html', {'msg': 'Password or Username Incorrect'})

    # 根据当前用户信息获取此用户所拥有的所有权限 并放入session
    # 获取当前用户所有权限
    init_permission(user_obj, request)
    return redirect('/customer/list/')


def register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save()
            new_user.password = user_register_form.cleaned_data['password']
            new_user.save()
            return redirect('/login/')
        else:
            print(user_register_form.errors)
            context = {
                'user':user_register_form
            }
            return render(request, 'register.html', context)
    if request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {
            'form':user_register_form
        }
        return render(request, 'register.html', context)


def user_logout(request):
    logout(request)
    return redirect('/login/')