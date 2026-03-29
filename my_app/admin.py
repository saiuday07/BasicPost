from django.contrib import admin
# Register your models here.
from .models import post

class PostAdmin(admin.ModelAdmin):
    list_display=['title','author','created_at','updated_at']

admin.site.register(post,PostAdmin)
