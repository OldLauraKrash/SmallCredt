from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'main.views.home', name='home'),
    url(r'^login/$', 'main.views.login', name='login'),
    url(r'^logout/$', 'main.views.logout', name='logout'),   
    url(r'^profile/$', 'client.views.profile', name='profile'),
    url(r'^register/$', 'main.views.register', name='register'),

    # url(r'^small_business/', include('small_business.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^.uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root':'.uploads/'}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':'./media/'}),
)
