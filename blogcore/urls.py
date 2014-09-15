from django.conf.urls import patterns, url
from blogcore import views

urlpatterns = patterns('',
                       url(r'^$', views.IndexView.as_view(), name = 'index'),
                       url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name = 'detail'),
                       url(r'^user$', views.UserListView.as_view(), name='userlist'),
                       url(r'^user/(?P<pk>\d+)/$', views.UserDetailView.as_view(), name='userdetail'),
                       url(r'^about/$', views.AboutView.as_view(), name = 'about'),
                       url(r'^register/$', views.RegisterView.as_view(), name = 'register'),
                       )