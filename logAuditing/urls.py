from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'log_main.views.index', name='home'),
    url(r'^login/(\w+)/$', 'log_main.views.login', name='login'),
    url(r'^ajax_refresh_log/$', 'log_main.views.ajax_refresh_log', name='ajax-refresh-log'),
    url(r'^ajax_save_log/$', 'log_main.views.ajax_save_log', name='ajax-save-log'),
    url(r'^ajax_check_all/(\w+)/$', 'log_main.views.ajax_check_all', name='ajax-check-all'),
    url(r'^ajax_check/(\d+)/$', 'log_main.views.ajax_check', name='ajax-check'),

    url(r'^admin/', include(admin.site.urls)),
)

