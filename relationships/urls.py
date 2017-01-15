from django.conf.urls import url, include
from api import urls as api_urls

urlpatterns = [
    url(r'^api/', include(api_urls, namespace='api')),
]
