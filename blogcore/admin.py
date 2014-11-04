from django.contrib import admin
from blogcore.models import UserProfile, Post, Comment

class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 1

class PostInLine(admin.TabularInline):
    inlines = [CommentInLine]
    model = Post
    extra = 1
    
class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInLine]
    search_fields = ['title']

class ProfileAdmin(admin.ModelAdmin):
    inlines = [PostInLine]

admin.site.register(UserProfile, ProfileAdmin)
admin.site.register(Post, PostAdmin)