from django.db import models


class Customer(models.Model):
    name = models.CharField(verbose_name='Name', max_length=32)
    age = models.CharField(verbose_name='Age', max_length=32)
    email = models.EmailField(verbose_name='Email', max_length=32)
    company = models.CharField(verbose_name='Company', max_length=32)

    def __str__(self):
        return self.name


class Payment(models.Model):

    customer = models.ForeignKey(verbose_name='Customer', to='Customer', on_delete=models.CASCADE)
    money = models.IntegerField(verbose_name='Payment')
    create_time = models.DateTimeField(verbose_name='Payment Date', auto_now_add=True)


