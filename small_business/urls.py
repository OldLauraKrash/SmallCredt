from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'main.views.home', name='home'),
    url(r'^login/$', 'main.views.login', name='login'),
    url(r'^logout/$', 'main.views.logout', name='logout'), 
    url(r'^forget_send/$', 'main.views.forget_send', name='forget_send'),  
    url(r'^forget/([-\w]*)/$', 'main.views.forget', name='forget'), 
    url(r'^active/([-\w]*)/$', 'main.views.active_account', name='active_account'),        
    url(r'^auth/$', 'client.views.auth', name='auth'),   
    url(r'^profile/$', 'client.views.profile', name='profile'),
    url(r'^account/credit-offers/$', 'client.views.credit_offers', name='credit_offers'),
    url(r'^account/$', 'client.views.account', name='account'),
    url(r'^qualify/$', 'client.views.qualify', name='qualify'),
    url(r'^profile/accepted/$', 'client.views.accepted', name='accepted'),
    url(r'^get-legal-form/$', 'client.views.get_legal_form', name='get_legal_form'),
    url(r'^get-state/$', 'client.views.get_state', name='get_state'),
    url(r'^get-country/$', 'client.views.get_country', name='get_country'),
    url(r'^get-industry/$', 'client.views.get_industry', name='get_industry'),
    url(r'^account/statements/$', 'client.views.statements', name='statements'),
    url(r'^profile/save-files/$', 'client.views.save_files', name='save_files'),
    url(r'^save-profile-main/$', 'client.views.save_profile_main', name='save_profile_main'),
    url(r'^save-profile-business/$', 'client.views.save_profile_business', name='save_profile_business'),
    url(r'^save-profile-credit/$', 'client.views.save_profile_credit', name='save_profile_credit'), 
    url(r'^register/$', 'main.views.register', name='register'),
    # url(r'^small_business/', include('small_business.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^.uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root':'.uploads/'}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':'./media/'}),
    url('^pages/', include('django.contrib.flatpages.urls')),
)
