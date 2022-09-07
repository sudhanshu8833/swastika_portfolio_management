from django.db import models
from django.db.models.fields import DateField, IntegerField
from django.contrib.auth.models import User
# Create your models here.



class User1(models.Model):

    username=models.CharField(max_length=50,default='SOME STRING')
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=25)
    
    angel_api_keys=models.CharField(max_length=100,default='SOME STRING')
    angel_client_id=models.CharField(max_length=10,default='SOME STRING')
    angel_password=models.CharField(max_length=10,default='SOME STRING')
    working_days_1=models.IntegerField(default=0)
    working_days_2=models.IntegerField(default=0)
    expiry_1=models.CharField(default="NA",max_length=12)
    expiry_2=models.CharField(default="NA",max_length=12)


class strategy(models.Model):

    strategy_id=models.CharField(default="0",max_length=20)
    buy_factor=models.IntegerField(default=300)
    sell_factor=models.IntegerField(default=0)
    TP1=models.IntegerField(default=40)
    TP2=models.IntegerField(default=90)
    time_out=models.IntegerField(default=60)
    percentage_premium=models.FloatField(default=0.99)
    lot=models.IntegerField(default=1)
    LIMIT=models.CharField(default="off",max_length=8)
    status=models.CharField(default="OPEN",max_length=8)
    working_days_1=models.IntegerField(default=0)
    working_days_2=models.IntegerField(default=0)
    expiry_1=models.CharField(default="NA",max_length=12)
    expiry_2=models.CharField(default="NA",max_length=12)

    T1=models.FloatField(default=0)
    T2=models.FloatField(default=0)
    T3=models.FloatField(default=0)
    T4=models.FloatField(default=0)
    T5=models.FloatField(default=0)
    T_now=models.IntegerField(default=3)

    expiry_selected=models.IntegerField(default=0)
    spot=models.FloatField(default=0)
    ET=models.FloatField(default=0)
    v_factor=models.FloatField(default=0)

    # sleep_time=models.IntegerField(default=0)

class orders(models.Model):

    strategy_id=models.CharField(max_length=20)
    symbol=models.CharField(max_length=20)
    time=models.DateTimeField(auto_now = True)
    price=models.FloatField(default=0)
    transaction_type=models.CharField(max_length=10)
    open_position=models.BooleanField(default=True)
    order_id=models.CharField(max_length=100)

class positions(models.Model):

    strategy_id=models.CharField(max_length=20,default='NA')
    symbol=models.CharField(max_length=20,default='NA')
    time_in=models.DateTimeField(auto_now_add = True)
    price_in=models.FloatField(default=0)
    side = models.CharField(max_length=20,default='NA')
    current_price=models.FloatField(default=0)
    time_out=models.DateTimeField(default=0)
    price_out=models.FloatField(default=0)
    status=models.CharField(max_length=20,default='NA')
    token=models.CharField(max_length=20,default='NA')