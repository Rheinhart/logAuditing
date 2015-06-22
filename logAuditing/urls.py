from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'log_main.views.index', name='home'),
    url(r'^ajax_refreshLog/$', 'log_main.views.ajax_refreshLog', name='ajax-refreshLog'),
    url(r'^ajax_checkall/$', 'log_main.views.ajax_checkAll', name='ajax-checkAll'),
    url(r'^ajax_check/$', 'log_main.views.ajax_check', name='ajax-check'),
    url(r'^ajax_dict/$', 'log_main.views.ajax_dict', name='ajax-dict'),

    url(r'^admin/', include(admin.site.urls)),
)

