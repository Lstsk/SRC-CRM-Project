from django.template import Library
from django.conf import settings
from collections import OrderedDict
from django.urls import reverse
from django.http import QueryDict
from rbac.service.url import previous_url_reverse
import re

register = Library()

@register.inclusion_tag('rbac/static_menu.html')
def static_menu(request):
    menu_list = request.session[settings.MENU_SESSION_KEY]
    return {'menu_list': menu_list}


@register.inclusion_tag('rbac/multi_menu.html')
def multi_menu(request):
    menu_dict = request.session[settings.MENU_SESSION_KEY]

    key_list = sorted(menu_dict)

    order_dict = OrderedDict()
    current_path = request.path

    for key in key_list:
        menu = menu_dict[key]
        menu['class'] = 'hide'

        for second_menu in menu['second_menu']:
            regex = f'^{second_menu["url"]}$'
            if re.match(regex, current_path):
                second_menu['class'] = 'active'
                menu['class'] = ''
        order_dict[key] = menu

    return {'menus': order_dict}


@register.inclusion_tag('rbac/breadcrumb.html')
def breadcrumb(request):
    return {'record_list': request.breadcrumb}


@register.filter
def has_permission(request, name):
    if name in request.session['setting.PERMISSION_SESSION_KEY']:
        return True

@register.simple_tag
def last_url(request, name, *args, **kwargs):
    return previous_url_reverse(request, name, *args, **kwargs)

