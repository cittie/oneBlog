from django.conf.urls import patterns, url
from blogcore import views
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
                       url(r'^$', views.IndexView.as_view(), name = 'index'),
                       url(r'^posts/$', views.PostListView.as_view(), name = 'post_list'),
                       url(r'^posts/create/$', views.PostCreateView.as_view(), name = 'post_create'), 
                       url(r'^post/(?P<pk>\d+)/$', views.PostDetailView.as_view(), name = 'post_detail'),
                       url(r'^post/(?P<pk>\d+)/edit/$', views.PostUpdateView.as_view(), name = 'post_edit'),                       
                       url(r'^profiles/$', views.UserListView.as_view(), name = 'profile_list'),
                       url(r'^profile/(?P<pk>\d+)/$', views.UserDetailView.as_view(), name = 'profile_detail'),
                       url(r'^about/$', views.AboutView.as_view(), name = 'about'),
                       url(r'^register/$', views.register, name = 'register'),
                       url(r'^login/$', login, name = 'login'),
                       url(r'^logout/$', logout, {'next_page': '/blogcore/login'}, name = 'logout'),
                       )