from django.shortcuts import render
from django.views import generic
from blogcore.models import Post, Comment
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = "blogcore/index.html"
    context_object_name = "blog_list"
    
    def get_queryset(self):
        return Post.objects.order_by("-created_date")[:10]

class DetailView(generic.DetailView):
    model = Post
    template_name = "blogcore/detail.html"
    
    def get_queryset(self):
        return Post.objects.filter(created_date__lte = timezone.now())
