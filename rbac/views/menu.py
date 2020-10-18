from django.shortcuts import render,redirect, HttpResponse
from rbac import models
from rbac.forms.menu import MenuModelForm, SecondMenuModelForm, PermissionModelForm, MultiAddPermissionForm, MultiEditPermissionForm
from django.urls import reverse
from rbac.service.url import previous_url
from django.forms import formset_factory


def menu_list(request):
    menus = models.Menu.objects.all()
    mid = request.GET.get('mid')
    sid = request.GET.get('sid')
    print(sid)

    menu_id_exits = models.Menu.objects.filter(id=mid).exists()
    sid_exits = models.Permission.objects.filter(id=sid).exists()

    if not sid_exits:
        sid = None

    if not menu_id_exits:
        mid = None

    if mid:
        level_two_menu = models.Permission.objects.filter(menu_id=mid)
    else:
        level_two_menu = []

    if sid:
        permissions = models.Permission.objects.filter(pid_id=sid)
    else:
        permissions = []

    context = {"menus": menus,
               "mid":mid,
               'level_two_menu': level_two_menu,
               'menu_if_exits': menu_id_exits,
               'sid':sid,
               'permissions':permissions,
               }

    return render(request, 'rbac/menu_list.html', context)


def menu_add(request):
    if request.method == 'POST':
        form = MenuModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(previous_url(request, 'rbac:menu_list'))
        context = {
            'form': form
        }
        return render(request, 'rbac/change.html', context)

    if request.method == 'GET':
        form = MenuModelForm()
        context = {
            'form': form
        }
        return render(request, 'rbac/change.html', context)


def menu_edit(request, id):
    obj = models.Menu.objects.filter(id=id).first()
    if not obj:
        return HttpResponse('404菜单不存在')
    if request.method == 'GET':
        form = MenuModelForm(instance=obj)
        context = {
            'form': form
        }
        return render(request, 'rbac/change.html', context)

    elif request.method == 'POST':
        form = MenuModelForm(instance=obj, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(previous_url(request, 'rbac:menu_list', ))
        else:
            context = {
                'form': form
            }
            return render(request, 'rbac/change.html', context)


def menu_del(request, id):
    base_url = previous_url(request, 'rbac:menu_list')

    if request.method == 'GET':
        context = {
            'cancel': base_url
        }
        return render(request, 'rbac/delete.html', context)
    if request.method == 'POST':
        models.Menu.objects.filter(id=id).delete()
        return redirect(base_url)


def second_menu_add(request, mid):

    menu_obj = models.Menu.objects.filter(id=mid).first()

    if request.method == 'POST':
        form = SecondMenuModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(previous_url(request, 'rbac:menu_list'))
        context = {
            'form': form
        }
        return render(request, 'rbac/change.html', context)

    if request.method == 'GET':
        form = SecondMenuModelForm(initial={'menu':menu_obj})
        context = {
            'form': form
        }
        return render(request, 'rbac/change.html', context)


def second_menu_edit(request, id):
    permission_obj = models.Permission.objects.filter(id=id).first()
    if not permission_obj:
        return HttpResponse('404菜单不存在')
    if request.method == 'GET':
        form = SecondMenuModelForm(instance=permission_obj)
        context = {
            'form': form
        }
        return render(request, 'rbac/change.html', context)

    elif request.method == 'POST':
        form = SecondMenuModelForm(instance=permission_obj, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(previous_url(request, 'rbac:menu_list', ))
        else:
            context = {
                'form': form
            }
            return render(request, 'rbac/change.html', context)


def second_menu_del(request, id):
    base_url = previous_url(request, 'rbac:menu_list')

    if request.method == 'GET':
        context = {
            'cancel': base_url
        }
        return render(request, 'rbac/delete.html', context)
    if request.method == 'POST':
        models.Permission.objects.filter(id=id).delete()
        return redirect(base_url)


def permission_add(request, sid):

    if request.method == 'POST':
        form = PermissionModelForm(data=request.POST)
        if form.is_valid():
            second_menu_object = models.Permission.objects.filter(id=sid).first()
            if not second_menu_object:
                return HttpResponse('Level-Two Menu Does Not Exists')

            form.instance.pid = second_menu_object
            form.save()
            return redirect(previous_url(request, 'rbac:menu_list'))
        context = {
            'form': form
        }
        return render(request, 'rbac/change.html', context)

    if request.method == 'GET':
        form = PermissionModelForm()
        context = {
            'form': form
        }
        return render(request, 'rbac/change.html', context)



def permission_edit(request, id):
    permission_obj = models.Permission.objects.filter(id=id).first()
    if not permission_obj:
        return HttpResponse('404菜单不存在')
    if request.method == 'GET':
        form = PermissionModelForm(instance=permission_obj)
        context = {
            'form': form
        }
        return render(request, 'rbac/change.html', context)

    elif request.method == 'POST':
        form = PermissionModelForm(instance=permission_obj, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(previous_url(request, 'rbac:menu_list', ))
        else:
            context = {
                'form': form
            }
            return render(request, 'rbac/change.html', context)


def permission_del(request, id):
    base_url = previous_url(request, 'rbac:menu_list')

    if request.method == 'GET':
        context = {
            'cancel': base_url
        }
        return render(request, 'rbac/delete.html', context)
    if request.method == 'POST':
        models.Permission.objects.filter(id=id).delete()
        return redirect(base_url)


import re
from collections import OrderedDict

from django.conf import settings
from django.utils.module_loading import import_string  # 根据字符串的形式，帮我们去导入模块
from django.urls import URLPattern, URLResolver  # 路由分发：URLResolver。不是路由分发：URLPattern


def check_url_exclude(url):
    for regex in settings.URLS_EXCLUDE:
        if re.match(regex, url):
            return True


def recursion_urls(pre_namespace, pre_url, urlpatterns, url_ordered_dict):

    for item in urlpatterns:
        if isinstance(item, URLPattern):
            if not item.name:
                continue
            if pre_namespace:
                name = f"{pre_namespace}:{item.name}"
            else:
                name = item.name
            url = pre_url + item.pattern.regex.pattern
            url = url.replace('^', '').replace('$', '')
            if check_url_exclude(url):
                continue
            url_ordered_dict[name] = {'name': name, 'url': url}


        elif isinstance(item, URLResolver):  # 路由分发，进行递归操作
            if pre_namespace:
                if item.namespace:
                    namespace = f"{pre_namespace}:{item.namespace}"

                else:
                    namespace = item.namespace
            else:
                if item.namespace:
                    namespace = item.namespace
                else:
                    namespace = None
            recursion_urls(namespace, pre_url + item.pattern.regex.pattern, item.url_patterns, url_ordered_dict)


def get_all_url_dict():
    url_ordered_dict = OrderedDict()
    md = import_string(settings.ROOT_URLCONF)


    recursion_urls(None, '/', md.urlpatterns, url_ordered_dict)
    return url_ordered_dict


def multi_permissions(request):
    post_type = request.GET.get('type')
    formset_add_class = formset_factory(MultiAddPermissionForm, extra=0)
    update_formset_class = formset_factory(MultiEditPermissionForm, extra=0)
    gen_formset = None
    update_formset = None

    if request.method == 'POST' and post_type == 'generate':
        formset = formset_add_class(data=request.POST)
        if formset.is_valid():
            object_list = []
            post_row_list = formset.cleaned_data
            has_error = False
            for i in range(0,formset.total_form_count()):
                row_dict = post_row_list[i]
                try:
                    new_object = models.Permission(**row_dict)
                    new_object.validate_unique()
                    object_list.append(new_object)
                except Exception as e:
                    formset.errors[i].update(e)
                    gen_formset = formset
                    has_error = True
            if not has_error:
                models.Permission.objects.bulk_create(object_list, batch_size=formset.total_form_count())

        else:
            gen_formset = formset

    if request.method == 'POST' and post_type == 'update':
        formset = update_formset_class(data=request.POST)
        if formset.is_valid():
            url_form_list = formset.cleaned_data
            for num in range(0, formset.total_form_count()):
                url_form = url_form_list[num]
                permission_id = url_form.pop('id')
                try:
                    permission_obj = models.Permission.objects.filter(id=permission_id).first()
                    for key, value in url_form.items():
                        setattr(permission_obj, key, value)
                    permission_obj.validate_unique()
                    permission_obj.save()
                except Exception as e:
                    formset.errors[num].update(e)
                    update_formset = formset
        else:
            update_formset = formset


    urls_dict = get_all_url_dict()
    print(urls_dict)
    router_name_set = set(urls_dict.keys())

    # for k, v in urls_dict.items():
    #     print(k, v)

    permissions = models.Permission.objects.all().values('id', 'title','url', 'name', 'menu_id', 'pid_id')
    print(permissions)
    permissions_dict = OrderedDict()
    permission_name_set = set()
    # print(permissions_dict)
    for permission in permissions:
        permissions_dict[permission['name']] = permission
        permission_name_set.add(permission['name'])
    # permission_name_set = set(permissions_dict.keys())

    for name,value in permissions_dict.items():
        router_row_dict = urls_dict.get(name)
        if not router_row_dict:
            continue
        # print(value['url'])
        if value['url'] != router_row_dict['url']:
            value['url'] = 'Url and database is not the same'
    if not gen_formset:
        gen_name_list = router_name_set - permission_name_set
        # {'name':'rbac:role_list', 'url': '/rbac/role/list'}, {'name': 'rbac:role_add', 'url': '/rbac/role/add'}
        gen_formset = formset_add_class(initial=[row_dict for name,row_dict in urls_dict.items() if name in gen_name_list ])

    delete_name_list = permission_name_set - router_name_set
    delete_row_list = [row_dict for name,row_dict in permissions_dict.items() if name in delete_name_list]

    if not update_formset:
        update_name_list = permission_name_set & router_name_set
        update_formset = update_formset_class(initial = [row_dict for name, row_dict in permissions_dict.items() if name in update_name_list])

    context = {
        'gen_formset': gen_formset,
        'del_row_list': delete_row_list,
        'update_formset': update_formset
    }
    return render(request, 'rbac/multi_permissions.html', context)



def multi_permissions_del(request, id):
    url = previous_url(request, 'rbac:multi_permissions')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel':url})

    if request.method == 'POST':
        models.Permission.objects.filter(id=id).delete()
        return redirect(url)


def distribute_permissions(request):
    uid = request.GET.get('uid')
    user_object = models.UserInfo.objects.filter(id=uid).first()
    if not user_object:
        uid = None

    rid = request.GET.get('rid')
    role = models.Role.objects.filter(id=rid).first()
    if not role:
        rid = None

    if request.method == 'POST' and request.POST.get('type') == 'role':
        roles_id_list = request.POST.getlist('roles')
        if not user_object:
            return HttpResponse('Please select a user')
        user_object.roles.set(roles_id_list)

    if request.method == 'POST' and request.POST.get('type') == 'permission':
        permission_id_list = request.POST.getlist('permissions')
        if not role:
            return HttpResponse('Please Pick A Role First')
        role.permissions.set(permission_id_list)


    # getting the roles from the uid
    if uid:
        user_roles = user_object.roles.all()
    else:
        user_roles = []
    user_roles_dict = {item.id: None for item in user_roles}

    # If choose the role id render the permission of the role
    if role:
        user_permissions = role.permissions.all()
        user_permissions_dict = {item.id: None for item in user_permissions}
    # return the users all permissions if only have uid
    elif user_object:
        user_permissions = user_object.roles.filter(permissions__id__isnull=False).values('id', 'permissions').distinct()
        user_permissions_dict = {item['permissions']: None for item in user_permissions}
    else:
        user_permissions = []
        user_permissions_dict = {}


    user_list = models.UserInfo.objects.all()
    row_list = models.Role.objects.all()
    menu_permission_list = []
    all_level_one_menu_list = models.Menu.objects.values('id', 'title')

    all_menu_dict = {}
    for item in all_level_one_menu_list:
        item['children'] = []
        all_menu_dict[item['id']] = item

    # Permission Able to be Menu
    all_level_two_menu_list = models.Permission.objects.filter(menu__isnull=False).values('id', 'title', 'menu_id')
    all_level_two_menu_dict = {}
    for second_menu in all_level_two_menu_list:
        second_menu['children'] = []
        all_level_two_menu_dict[second_menu['id']] = second_menu
        menu_id = second_menu['menu_id']
        all_menu_dict[menu_id]['children'].append(second_menu)

    # Permission not able to be menu
    all_level_three_menu_list = models.Permission.objects.filter(menu__isnull=True).values('id', 'title', 'pid_id')

    for permission in all_level_three_menu_list:
        pid = permission['pid_id']
        if not pid:
            continue
        all_level_two_menu_dict[pid]['children'].append(permission)


    # print(all_level_one_menu_list)
    context = {
        'user_list':user_list,
        'role_list': row_list,
        'all_menu_list': all_level_one_menu_list,
        'uid':uid,
        'user_roles':user_roles_dict,
        'user_permissions': user_permissions_dict,
        'rid':rid
    }

    return render(request, 'rbac/distribute_permissions.html', context)









"""
[{
	'id': 1,
	'title': 'Information Management',
	'children': [{
		'id': 4,
		'title': 'Import Many',
		'menu_id': 1,
		'children': []
	}, {
		'id': 15,
		'title': 'Role List',
		'menu_id': 1,
		'children': []
	}, {
		'id': 19,
		'title': 'User List',
		'menu_id': 1,
		'children': []
	}, {
		'id': 24,
		'title': 'Menu List',
		'menu_id': 1,
		'children': []
	}, {
		'id': 28,
		'title': 'Two-Level Add',
		'menu_id': 1,
		'children': []
	}, {
		'id': 31,
		'title': 'Permission Add',
		'menu_id': 1,
		'children': []
	}]
}, {
	'id': 2,
	'title': 'User Management',
	'children': [{
		'id': 1,
		'title': 'Customer List',
		'menu_id': 2,
		'children': [{
			'id': 2,
			'title': 'Add Customer1',
			'pid_id': 1
		}, {
			'id': 3,
			'title': 'Edit Customer',
			'pid_id': 1
		}, {
			'id': 6,
			'title': 'Download template',
			'pid_id': 1
		}]
	}]
}, {
	'id': 3,
	'title': 'Payments',
	'children': [{
		'id': 7,
		'title': 'Payments',
		'menu_id': 3,
		'children': [{
			'id': 8,
			'title': 'Add Payment',
			'pid_id': 7
		}, {
			'id': 9,
			'title': 'Edit Payments',
			'pid_id': 7
		}, {
			'id': 10,
			'title': 'Delete Payment',
			'pid_id': 7
		}]
	}]
}]

"""