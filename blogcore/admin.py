from django.contrib import admin
from blogcore.models import Post, Comment

class CommentInLine(admin.TabularInline):
    model = Comment

class PostAdmin(admin.ModelAdmin):
    fields_sets = [
                   (None,   {'fields' : ['title', 'content']}),
                   ('Time', {'fields' : ['created_date']}),
                   ]
    inlines = [CommentInLine]
    list_display = ('title', 'content', 'created_date')
    search_fields = ['title']

admin.site.register(Post, PostAdmin)
