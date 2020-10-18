from django.urls import reverse
from django.http import QueryDict


def previous_url(request, name, *args, **kwargs):
    base_url = reverse('rbac:menu_list')
    orginal_param = request.GET.get('_filter')
    if orginal_param:
        base_url = f'{base_url}?{orginal_param}'
    return base_url


def previous_url_reverse(request, name, *args, **kwargs):
    original_url = reverse(name, args=args, kwargs=kwargs)
    if not request.GET:
        return original_url
    else:
        query_dict = QueryDict(mutable=True)

        old_get_param = request.GET.urlencode()
        query_dict['_filter'] = old_get_param
        tpl = f'{original_url}?{query_dict.urlencode()}'
        return tpl
