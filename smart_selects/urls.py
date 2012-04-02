from django.conf.urls.defaults import *

urlpatterns = patterns('smart_selects.views',
    url(r'^all/(?P<app>[\w\-]+)/(?P<model>[\w\-]+)/(?P<field>[\w\-]+)/(?P<value>[\w\-]+)/$', 'filterchain_all', name='chained_filter_all'),
    url(r'^filter/(?P<app>[\w\-]+)/(?P<model>[\w\-]+)/(?P<field>[\w\-]+)/(?P<value>[\w\-]+)/$', 'filterchain', name='chained_filter'),
    url(r'^filter/(?P<app>[\w\-]+)/(?P<model>[\w\-]+)/(?P<manager>[\w\-]+)/(?P<field>[\w\-]+)/(?P<value>[\w\-]+)/$', 'filterchain', name='chained_filter'),
    url(r'^subfilter/(?P<app>[\w\-]+)/(?P<model>[\w\-]+)/(?P<field>[\w\-]+)/(?P<submodel>[\w\-]+)/(?P<subfield>[\w\-]+)/(?P<value>[\w\-]+)/$', 'filtersubchain', name='chained_subfilter'),
    url(r'^subfilter/(?P<app>[\w\-]+)/(?P<model>[\w\-]+)/(?P<manager>[\w\-]+)/(?P<field>[\w\-]+)/(?P<submodel>[\w\-]+)/(?P<subfield>[\w\-]+)/(?P<value>[\w\-]+)/$', 'filtersubchain', name='chained_subfilter'),
)
