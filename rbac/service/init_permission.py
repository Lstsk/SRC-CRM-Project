from django.conf import settings


def init_permission(user_obj, request):
    user_permission = user_obj.roles.filter(permissions__isnull=False).values("permissions__id",
                                                                              "permissions__title",
                                                                              "permissions__menu__icon",
                                                                              "permissions__url",
                                                                              "permissions__menu__title",
                                                                              "permissions__menu",
                                                                              "permissions__pid_id",
                                                                              "permissions__pid__title",
                                                                              "permissions__pid__url",
                                                                              "permissions__name").distinct()
    print(user_obj.roles.values('permissions__menu'))
    menu_dict = {}
    print(user_permission)
    permission_dict = {}

    for item in user_permission:
        permission_dict[item['permissions__name']] = {
            'id': item['permissions__id'],
            'url': item['permissions__url'],
            'title': item['permissions__title'],
            'pid': item['permissions__pid_id'],
            'p_title': item['permissions__pid__title'],
            'p_url': item['permissions__pid__url']
        }

        menu_id = item['permissions__menu']
        print('hi')
        if not menu_id:
            continue
        print('hio')
        second_menu = {'id': item['permissions__id'], 'title': item['permissions__title'], 'url': item['permissions__url']}
        if menu_id in menu_dict:
            menu_dict[menu_id]['second_menu'].append(second_menu)

        else:
            print('hi')
            menu_dict[menu_id] = {
                'title': item['permissions__menu__title'],
                'icon': item['permissions__menu__icon'],
                'second_menu': [second_menu, ]
            }
    #     print(menu_id)
    # print(menu_dict)
    # print('hi')
    # if item['permissions__is_menu']:
    #     temp = {
    #         'title': item['permissions__title'],
    #         'icon': item['permissions__icon'],
    #         'url': item["permissions__url"]
    #     }
    #     menu_list.append(temp)
    #  save to session
    print(permission_dict)
    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict
    request.session[settings.MENU_SESSION_KEY] = menu_dict
    print(request.session[settings.MENU_SESSION_KEY])
    print(menu_dict)
    print('done')
    print(request.session[settings.PERMISSION_SESSION_KEY])

# {1: {'title': 'Information Management', 'icon': 'fa-camera-retro', 'children': [{'title': 'Customer List', 'url': '/customer/list/'}]},
#  2: {'title': 'User Management', 'icon': 'fa-user-circle', 'children': [{'title': 'Payments', 'url': '/payment/list/'}]}}

"""
"""