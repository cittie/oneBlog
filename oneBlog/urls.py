from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'oneBlog.views.home', name='home'),
    url(r'^blogcore/', include('blogcore.urls', namespace = 'blogcore')),
    url(r'^admin/', include(admin.site.urls)),
)
