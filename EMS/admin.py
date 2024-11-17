from django.contrib import admin

# Register your models here.

from .models import EventData,Comment,Image,SeatingImage,ScheduleImage

admin.site.register(EventData)
admin.site.register(Comment)
admin.site.register(Image)
admin.site.register(ScheduleImage)
admin.site.register(SeatingImage)
