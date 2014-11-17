from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from blogcore.models import Post, UserProfile, PostForm, CommentForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class IndexView(ListView):
    template_name = "blogcore/index.html"
    context_object_name = "post_list"
    
    def get_queryset(self):
        return Post.objects.order_by("-created_date")[:10]
    
class PostListView(ListView):
    template_name = "blogcore/posts.html"
    context_object_name = "post_list"
    
    def get_queryset(self):
        return Post.objects.order_by("-created_date")[:10]

class PostDetailView(DetailView):
    model = Post
    template_name = "blogcore/postdetail.html"

class UserListView(ListView):
    template_name = "blogcore/users.html"
    context_object_name = "profile_list"
    
    def get_queryset(self):
        return UserProfile.objects.order_by("-id")[:10]

class UserDetailView(DetailView):
    model = UserProfile
    template_name = "blogcore/userdetail.html"
    context_object_name = "user_profile"

class AboutView(TemplateView):
    template_name = "blogcore/about.html"

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            UserProfile.objects.create(user = new_user)            
            return redirect('blogcore:profile_list')
    else:
        form = UserCreationForm()
    return render(request, 'blogcore/register.html', {'form': form})

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "blogcore/postcreate.html"
    
    def form_valid(self, form):
        post = form.save(commit = False)
        post.user_profile = UserProfile.objects.get(user = self.request.user)
        post.save()
        return redirect('blogcore:profile_list')
