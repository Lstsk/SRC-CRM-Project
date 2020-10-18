from django.http import request
from django.test import TestCase

# Create your tests here.
import os
import sys


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm project.settings")
    import django
    django.setup()

    from rbac.middlewares.rbac import RbacMiddleware




