"""
Role management
"""
from rbac import models
from django.shortcuts import render, redirect,HttpResponse
from django.urls import reverse
from rbac.forms.user import UserModelForm, UpdateUserModelForm, ResetUserModelForm


def user_list(request):
    user_queryset = models.UserInfo.objects.all()

    content = {
        'users': user_queryset
    }

    return render(request, 'rbac/user_list.html', content)


def user_add(request):
    if request.method == 'POST':
        form = UserModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:user_list'))
        context = {
            'form': form
        }
        return render(request, 'rbac/change.html', context)

    if request.method == 'GET':
        form = UserModelForm()
        context = {
            'form': form
        }
        return render(request, 'rbac/change.html', context)


def user_edit(request, id):
    obj = models.UserInfo.objects.filter(id=id).first()
    if not obj:
        return HttpResponse('404用户不存在')
    if request.method == 'GET':
        form = UpdateUserModelForm(instance=obj)
        context = {
            'form': form
        }
        return render(request, 'rbac/change.html', context)

    elif request.method == 'POST':
        form = UpdateUserModelForm(instance=obj ,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:user_list'))
        else:
            context = {
                'form': form
            }
            return render(request, 'rbac/change.html', context)


def user_del(request, id):

    origin_url = reverse('rbac:user_list')
    if request.method == 'GET':
        context = {
            'cancel': origin_url
        }
        return render(request, 'rbac/delete.html', context)
    if request.method == 'POST':
        models.UserInfo.objects.filter(id=id).delete()
        return redirect(origin_url)


def user_reset_pwd(request, id):
    obj = models.UserInfo.objects.filter(id=id).first()
    if not obj:
        return HttpResponse('404用户不存在')
    if request.method == 'GET':
        form = ResetUserModelForm()
        context = {
            'form': form
        }
        return render(request, 'rbac/change.html', context)

    elif request.method == 'POST':
        form = ResetUserModelForm(instance=obj ,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:user_list'))
        else:
            context = {
                'form': form
            }
            return render(request, 'rbac/change.html', context)