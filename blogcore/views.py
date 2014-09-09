from django.shortcuts import render
from django.views import generic
from blogcore.models import Post, Comment

class IndexView(generic.ListView):
    template_name = "blogcore/index.html"
    context_object_name = "blog_list"
    
    def get_queryset(self):
        return Post.objects.all().order_by("-created_date")[:10]

class DetailView(generic.DetailView):
    template_name = "blogcore/detail.html"
    
    def get_queryset(self):
        return Post.objects.filter()
