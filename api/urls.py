from api import views
from rest_framework import routers
from django.conf.urls import url, include

router = routers.DefaultRouter()
router.register(r'sessions', views.SessionViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
