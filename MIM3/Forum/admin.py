from django.contrib import admin
from .models import *

# Model Admin allowing better viewing of model information
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("username","first_name", "last_name","membership")

# Register your models here.
admin.site.register(Organization)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post)
admin.site.register(Event)
admin.site.register(PostImage)
admin.site.register(Message)
admin.site.register(Bid)