from django.contrib import admin

# Register your models here.
from .models import EventData,Comment,Image,SeatingImage,ScheduleImage, Sponsor, EventDetail,Guest,Profile


# admin.site.register(EventData)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Image)
admin.site.register(ScheduleImage)
admin.site.register(SeatingImage)


class SponsorInline(admin.TabularInline):
    model = Sponsor
    extra = 1  # Number of extra blank fields for new sponsors

class EventDetailInline(admin.TabularInline):
    model = EventDetail
    extra = 1  # Number of extra blank fields for new details

class GuestInline(admin.TabularInline):
    model = Guest
    extra = 1  # Number of extra blank fields for new guests

@admin.register(EventData)
class EventDataAdmin(admin.ModelAdmin):
    inlines = [SponsorInline, EventDetailInline,GuestInline]
    list_display = ('name', 'category', 'start_date', 'end_date', 'created_date')
    search_fields = ('name', 'category', 'art_category')

