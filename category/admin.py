from django.contrib import admin


# from .models import Category, SubCategory, Apply
from .models import Category,Post,Tag,Comment,SubCategory,Apply

# Register your models here.



# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display=['id','title','author']
class TagAdmin(admin.ModelAdmin):
    list_display=['name','list_of_post']



# admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Tag,TagAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Apply)
