from django.contrib import admin

# Register your models here.

from .models import EventData,Comment,Image

admin.site.register(EventData)
admin.site.register(Comment)
admin.site.register(Image)
