from django.test import TestCase

# Create your tests here.
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm project.settings")
    import django
    django.setup()
    from rbac import models



    user_obj = models.UserInfo.objects.filter(id=1).first()

    user_permission = user_obj.roles.filter(permissions__isnull=False).values("permissions__id",
                                                                              "permissions__title",
                                                                              "permissions__is_menu",
                                                                              "permissions__icon",
                                                                              "permissions__url").distinct()
    for item in user_permission:
        print(item['permissions__url'])