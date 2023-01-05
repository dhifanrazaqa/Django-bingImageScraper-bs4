from django.contrib import admin
from .models import Post, imagePost

class videoInline(admin.TabularInline):
    model = imagePost

class PostAdmin(admin.ModelAdmin):
    inlines = [videoInline]

admin.site.register(Post, PostAdmin)
admin.site.register(imagePost)