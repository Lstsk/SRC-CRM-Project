from django.db import models


class Menu(models.Model):
    title = models.CharField(verbose_name='Level One Menu', max_length=32)
    icon = models.CharField(verbose_name='icon', max_length=32)

    def __str__(self):
        return self.title


class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(verbose_name='标题', max_length=32)
    url = models.CharField(verbose_name='含正则的URL', max_length=128)
    is_menu = models.BooleanField(verbose_name='Can it be a menu', default=False)
    # icon = models.CharField(verbose_name='icon', max_length=32, null=True, blank=True)
    name = models.CharField(verbose_name='other name of url', max_length=32, null=True)
    menu = models.ForeignKey(verbose_name='all menu', to=Menu, null=True, on_delete=models.CASCADE, help_text="null means no menu")
    pid = models.ForeignKey(verbose_name='connect none menu permission to a menu permission', help_text='to help show the menu when going to a non menu url', on_delete=models.CASCADE, to='Permission', related_name='parents')

    def __str__(self):
        return self.title


class Role(models.Model):
    """
    角色
    """
    title = models.CharField(verbose_name='角色名称', max_length=32)
    permissions = models.ManyToManyField(verbose_name='拥有的所有权限', to=Permission, blank=True)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """
    用户表
    """
    name = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    email = models.CharField(verbose_name='邮箱', max_length=32)
    roles = models.ManyToManyField(verbose_name='拥有的所有角色', to='Role', blank=True)
    image = models.ImageField(upload_to='media')

    def __str__(self):
        return self.name
