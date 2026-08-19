from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ProductViewSet,
    CustomerViewSet,
    OrderViewSet
)


router = DefaultRouter()

router.register(
    "products",
    ProductViewSet,
    basename="products"
)

router.register(
    "customers",
    CustomerViewSet,
    basename="customers"
)

router.register(
    "orders",
    OrderViewSet,
    basename="orders"
)


urlpatterns = [
    path("", include(router.urls)),
]