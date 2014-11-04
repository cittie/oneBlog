from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from blogcore.models import Post, UserProfile

from django.http import HttpResponseRedirect

class IndexView(generic.ListView):
    template_name = "blogcore/index.html"
    context_object_name = "post_list"
    
    def get_queryset(self):
        return Post.objects.order_by("-created_date")[:10]
    
class PostListView(generic.ListView):
    template_name = "blogcore/posts.html"
    context_object_name = "post_list"
    
    def get_queryset(self):
        return Post.objects.order_by("-created_date")[:10]

class PostDetailView(generic.DetailView):
    model = Post
    template_name = "blogcore/postdetail.html"

class UserListView(generic.ListView):
    template_name = "blogcore/users.html"
    context_object_name = "profile_list"
    
    def get_queryset(self):
        return UserProfile.objects.order_by("-id")[:10]

class UserDetailView(generic.DetailView):
    model = UserProfile
    template_name = "blogcore/userdetail.html"
    context_object_name = "user_profile"

class AboutView(generic.TemplateView):
    template_name = "blogcore/about.html"

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/books/")
    else:
        form = UserCreationForm()
    return render(request, "blogcore/register.html", {
        'form': form,
    })
 
def login_view(request):
    username = password = ''
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        user = authenticate(username = username, password = password)

        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect('/blogcore/user')
        else:
            return HttpResponseRedirect('/blogcore/about')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/blogcore/about')           

