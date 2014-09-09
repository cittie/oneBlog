from django.shortcuts import render
from django.views import generic
from blogcore.models import Post, Comment

class IndexView(generic.ListView):
    
    def get_queryset(self):
        return Post.objects.all()[:5]

class DetailView(generic.ListView):
    
    def get_queryset(self):
        return Post.objects.filter()