from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Blog, Comment, Profile

# Blog Admin Customization
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    list_filter = ('author',)
    search_fields = ('title', 'author__username')
    ordering = ('-created_at',)

# Comment Admin Customization
class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'author', 'text', 'created_at')
    search_fields = ('blog__title', 'author__username', 'text')
    ordering = ('-created_at',)

# Profile Inline for User Admin
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

# Custom User Admin with Profile
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

# Re-register User with Profile
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register other models
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Profile)
