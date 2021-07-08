from django.contrib import admin

from .models import User,Bid,Comment,Product
# Register your models here.

admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Product)
admin.site.register(Comment)