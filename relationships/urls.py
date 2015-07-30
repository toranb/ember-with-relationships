from django.conf.urls import include, url, patterns
from api import urls as api_urls

urlpatterns = patterns('',
    url(r'^api/', include(api_urls, namespace='api')),
)
