from django.contrib import admin
from blogcore.models import Bloguser, Post, Comment

class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 1

class PostInLine(admin.TabularInline):
    inlines = [CommentInLine]
    model = Post
    extra = 1
    
class BloguserAdmin(admin.ModelAdmin):
    fields = ('name', 'create_date')
    inlines = [PostInLine, CommentInLine]
    search_fields = ['name']

class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInLine]
    search_fields = ['title']
    
admin.site.register(Bloguser, BloguserAdmin)
admin.site.register(Post, PostAdmin)
