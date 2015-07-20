from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'log_main.views.index', name='home'),
    url(r'^login/(\w+)/$', 'log_main.views.login', name='login'),
    url(r'^ajax_refreshLog/$', 'log_main.views.ajax_refreshLog', name='ajax-refreshLog'),
    url(r'^ajax_saveLog/$', 'log_main.views.ajax_saveLog', name='ajax-saveLog'),
    url(r'^ajax_checkall/(\w+)/$', 'log_main.views.ajax_checkAll', name='ajax-checkall'),
    url(r'^ajax_check/(\d+)/$', 'log_main.views.ajax_check', name='ajax-check'),

    url(r'^admin/', include(admin.site.urls)),
)

