from django.conf.urls.defaults import patterns, include, url

from dates.views import current_datetime, hours_ahead
from pricer.views import pricer

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MVPricer.views.home', name='home'),
    # url(r'^MVPricer/', include('MVPricer.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^time/$', current_datetime),
    (r'^time/plus/(\d{1,2})', hours_ahead),
    (r'^$', pricer)
)
