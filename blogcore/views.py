from django.views import generic
from django import forms
from blogcore.models import Bloguser, Post, Comment
from django.shortcuts import render
from django.http import HttpResponseRedirect

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
    
class RegisterView(generic.TemplateView):
    template_name = "blogcore/register.html"    

class NameForm(forms.Form):
    register_name = forms.CharField(label = "Register Name", max_length = 16)
    
def get_register(request):
    if request.method == "POST":
        form = NameForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('blogcore/index.html')
    else:
        form = NameForm()
    
    return render(request, 'blogcore/register.html', {'form': form})
        
         
