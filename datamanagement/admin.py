from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(User1)
admin.site.register(strategy)
admin.site.register(orders)
admin.site.register(positions)