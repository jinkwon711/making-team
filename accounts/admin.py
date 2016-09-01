from django.contrib import admin

# Register your models here.
from .models import Profile

# Register your models here.



# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display=['user','gender','interest']


# admin.site.register(Post, PostAdmin)
admin.site.register(Profile)
