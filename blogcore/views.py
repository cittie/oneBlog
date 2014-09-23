from django.views import generic
from blogcore.models import Bloguser, Post
from blogcore.forms import LoginForm
#from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect

class IndexView(generic.ListView):
    template_name = "blogcore/index.html"
    context_object_name = "blog_list"
    
    def get_queryset(self):
        return Post.objects.order_by("-created_date")[:10]

class UserListView(generic.ListView):
    template_name = "blogcore/userlist.html"
    context_object_name = "bloguser_list"
    
    def get_queryset(self):
        return Bloguser.objects.order_by("-id")[:10]

class UserDetailView(generic.DetailView):
    model = Bloguser
    template_name = "blogcore/userdetail.html"
    context_object_name = "bloguser"

class DetailView(generic.DetailView):
    model = Post
    template_name = "blogcore/detail.html"

class AboutView(generic.TemplateView):
    template_name = "blogcore/about.html"
    
class RegisterCreate(generic.CreateView):
    template_name = "blogcore/register.html" 
    model = Bloguser
    field = ['name']
    success_url = '/blogcore/user'
   
def login_user(request):
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = authenticate(username = username, password = password)
        except:
            return HttpResponse("Error")
        else:
            if user.is_active:
                login(request, user)
                HttpResponseRedirect('/blogcore/user')
            else:
                return HttpResponse("Sorry!")
            
def test_view(request):
    
