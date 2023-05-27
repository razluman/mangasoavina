from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'apvs', views.ApvViewSet)

app_name = 'paroasy'
urlpatterns = [
    path('api/', include(router.urls)),
]
