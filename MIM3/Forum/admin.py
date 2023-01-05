from django.contrib import admin
from .models import *

# Model Admin allowing better viewing of model information
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("username","first_name", "last_name","membership")

class EventAdmin(admin.ModelAdmin):
    list_display = ("post", 'date', 'time', 'open')

# Register your models here.
admin.site.register(Organization)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post)
admin.site.register(Event, EventAdmin)
admin.site.register(PostImage)
admin.site.register(Message)
admin.site.register(Bid)