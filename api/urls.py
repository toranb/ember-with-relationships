from api import views
from rest_framework import routers
from django.conf.urls import include, url, patterns

router = routers.DefaultRouter()
router.register(r'sessions', views.SessionViewSet)

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
)
