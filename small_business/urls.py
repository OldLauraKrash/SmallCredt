from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from django.conf import settings
import os
admin.autodiscover()

def pie_with_headers(request):
    filename = settings.MEDIA_ROOT + 'css/PIE.htc'
    wrapper = FileWrapper(open(filename))
    response = HttpResponse(wrapper, content_type='text/x-component')
    response['Content-Length'] = os.path.getsize(filename)
    return response

def sitemap_with_headers(request):
    filename = settings.MEDIA_ROOT + 'sitemap.xml'
    wrapper = FileWrapper(open(filename))
    response = HttpResponse(wrapper, content_type='text/xml')
    response['Content-Length'] = os.path.getsize(filename)
    return response

urlpatterns = patterns('',
    url(r'^$', 'main.views.home', name='home'),
    url(r'^PIE.htc', pie_with_headers, {}),
    url(r'^login/$', 'main.views.login', name='login'),
    url(r'^logout/$', 'main.views.logout', name='logout'), 
    url(r'^forget_send/$', 'main.views.forget_send', name='forget_send'),  
    url(r'^forget/([-\w]*)/$', 'main.views.forget', name='forget'), 
    url(r'^active/([-\w]*)/$', 'main.views.active_account', name='active_account'),
    url(r'^page_not_found/$', 'main.views.page_not_found', name='page_not_found'),             
    url(r'^auth/$', 'client.views.auth', name='auth'),   
    url(r'^profile/$', 'client.views.profile', name='profile'),
    url(r'^account/credit-offers/$', 'client.views.credit_offers', name='credit_offers'),
    url(r'^account/$', 'client.views.account', name='account'),
    url(r'^account/finish$', 'client.views.finish_page', name='finish_page'),
    url(r'^account-finish/$', 'client.views.account_finish', name='account_finish'),
    url(r'^qualify/$', 'client.views.qualify', name='qualify'),
    url(r'^profile/accepted/$', 'client.views.accepted', name='accepted'),
    url(r'^get-legal-form/$', 'client.views.get_legal_form', name='get_legal_form'),
    url(r'^get-state/$', 'client.views.get_state', name='get_state'),
    url(r'^get-country/$', 'client.views.get_country', name='get_country'),
    url(r'^get-industry/$', 'client.views.get_industry', name='get_industry'),
    url(r'^get-geography/$', 'lender.views.get_geography', name='get_geography'),
    url(r'^get-risk-level/$', 'client.views.get_risk_level', name='get_risk_level'),
    url(r'^get-risk-lender/$', 'lender.views.get_risk_lender', name='get_risk_lender'),
    url(r'^account/statements/$', 'client.views.statements', name='statements'),
    url(r'^profile/save-files/$', 'client.views.save_files', name='save_files'),
    url(r'^save-profile-main/$', 'client.views.save_profile_main', name='save_profile_main'),
    url(r'^save-profile-business/$', 'client.views.save_profile_business', name='save_profile_business'),
    url(r'^save-profile-credit/$', 'client.views.save_profile_credit', name='save_profile_credit'), 
    url(r'^register/$', 'main.views.register', name='register'),
    url(r'^lender/account/$', 'lender.views.lender_account', name='lender_account'),   
    url(r'^lender/statements/$', 'lender.views.lender_statements', name='lender_statements'), 
    url(r'^lender/portfolio/$', 'lender.views.lender_portfolio', name='lender_portfolio'),
    url(r'^lender/marketplace/$', 'lender.views.lender_marketplace', name='lender_marketplace'),
    url(r'^lender/marketplace/bid/$', 'lender.views.bid', name='bid'),
    url(r'^lender/info/(?P<id>\d+)/$', 'lender.views.info', name='info'),   
    url(r'^lender/marketplace/decline/$', 'lender.views.decline', name='decline'),
    url(r'^lender/marketplace/borrower/(?P<id>\d+)/$', 'lender.views.lender_marketplace_borrower', name='lender_marketplace_borrower'),
    url(r'^save-lender/$', 'lender.views.save_lender', name='save_lender'),
    url(r'^lender/edit/$', 'lender.views.lender_edit', name='lender_edit'), 
    url(r'^lender/save-tag/$', 'lender.views.save_lender_tag', name='save_lender_tag'),    
    url(r'^lender/remove-item-tag/$', 'lender.views.remove_item_tag', name='remove_item_tag'),  
    url(r'^loan/accepted/$', 'loan.views.loan_accepted', name='loan_accepted'),  
    url(r'^loan/decline/$', 'loan.views.loan_decline', name='loan_decline'), 
    url(r'^loan/cancel/$', 'loan.views.loan_cancel', name='loan_cancel'),
    url(r'^api/connect/first/$', 'api.views.register_step_first', name='register_step_first'),
    url(r'^api/connect/second/$', 'api.views.register_step_second', name='register_step_second'),
    url(r'^api/connect/finish/$', 'api.views.register_step_finish', name='register_step_finish'),
    url(r'^api/get-institutions/$', 'api.views.get_institutions', name='get_institutions'),
    url(r'^remove-bank-file/(?P<id>\d+)/$', 'client.views.remove_bank_file', name='remove_bank_file'),
    url(r'^remove-processor-file/(?P<id>\d+)/$', 'client.views.remove_processor_file', name='remove_processor_file'),
    url(r'^remove-financial-file/(?P<id>\d+)/$', 'client.views.remove_financial_file', name='remove_financial_file'),   
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^.uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root':'.uploads/'}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':'./media/'}),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^sitemap.xml', sitemap_with_headers, {}),
)
handler500 = 'main.views.page_not_found'
handler404 = 'main.views.page_not_found'
