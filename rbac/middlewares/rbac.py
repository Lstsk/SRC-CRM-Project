import re
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse,redirect
from django.conf import settings


class RbacMiddleware(MiddlewareMixin):

    def process_request(self, request):
        current_url = request.path
        for valid_url in settings.VALID_URL_LIST:
            if re.match(valid_url, current_url):
                return None

        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        if not permission_dict:
            return redirect('/login/')

        flag = False

        url_record = [
            {'title': '首页', 'url': '#'}
        ]

        for item in permission_dict.values():
            reg = "^%s$" % item['url']
            if re.match(reg, current_url):
                flag = True
                request.current_selected_permission = item['pid'] or item['id']
                if not item['pid']:
                    url_record.extend([{'title': item['title'], 'url': item['url'], 'class': 'active'}])
                else:
                    url_record.extend([
                        {'title': item['p_title'], 'url': item['p_url']},
                        {'title': item['title'], 'url': item['url'], 'class': 'active'},
                    ])
                request.breadcrumb = url_record
                break

        if not flag:
            return HttpResponse('No Access')