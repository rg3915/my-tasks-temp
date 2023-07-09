from crm.views import CustomerViewSet
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'customers', CustomerViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
