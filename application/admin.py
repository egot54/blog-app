from django.contrib import admin
from .models import Blog, AccessRequest

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'approve_status', 'is_private', 'created']
    list_filter = ['approve_status', 'is_private']
    search_fields = ['title', 'author']

@admin.register(AccessRequest)
class AccessRequestAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'is_approved', 'created_at']
    list_filter = ['is_approved']