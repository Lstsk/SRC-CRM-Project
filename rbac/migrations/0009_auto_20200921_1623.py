# Generated by Django 2.2 on 2020-09-21 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0008_auto_20200905_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='menu',
            field=models.ForeignKey(help_text='null means no menu', null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.Menu', verbose_name='all menu'),
        ),
        migrations.AlterField(
            model_name='permission',
            name='pid',
            field=models.ForeignKey(help_text='to help show the menu when going to a non menu url', on_delete=django.db.models.deletion.CASCADE, related_name='parents', to='rbac.Permission', verbose_name='connect none menu permission to a menu permission'),
        ),
    ]