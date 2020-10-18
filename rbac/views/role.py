"""
Role management
"""
from rbac import models
from django.shortcuts import render, redirect,HttpResponse
from django.urls import reverse
from rbac.forms.role import RoleModelForm




def role_list(request):
    role_queryset = models.Role.objects.all()

    content = {
        'roles': role_queryset
    }

    return render(request, 'rbac/role_list.html', content)


def role_add(request):

    if request.method == 'POST':
        form = RoleModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:role_list'))

    if request.method == 'GET':
        form = RoleModelForm()
    context = {
            'form': form
        }
    return render(request, 'rbac/change.html', context)


def role_edit(request, id):
    obj = models.Role.objects.filter(id=id).first()
    if not obj:
        return HttpResponse('404角色不存在')
    if request.method == 'GET':
        form = RoleModelForm(instance=obj)
        context = {
            'form': form
        }
        return render(request, 'rbac/change.html', context)

    elif request.method == 'POST':
        form = RoleModelForm(instance=obj ,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:role_list'))
        else:
            context = {
                'form': form
            }
            return render(request, 'rbac/change.html', context)


def role_del(request, id):

    origin_url = reverse('rbac:role_list')
    if request.method == 'GET':
        context = {
            'cancel': origin_url
        }
        return render(request, 'rbac/delete.html', context)
    if request.method == 'POST':
        models.Role.objects.filter(id=id).delete()
        return redirect(origin_url)