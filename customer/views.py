from django.shortcuts import render

# Create your views here.
from django.db.models import Q

from rest_framework import viewsets

from .models import (
    Product,
    Customer,
    Order
)

from .serializers import (
    ProductSerializer,
    CustomerSerializer,
    OrderSerializer
)


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer

    def get_queryset(self):

        queryset = Product.objects.all().order_by(
            "-created_at"
        )

        search = self.request.query_params.get("search")

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(sku__icontains=search)
            )

        return queryset

class CustomerViewSet(
    viewsets.ModelViewSet
):

    queryset = Customer.objects.all().order_by(
        "-created_at"
    )

    serializer_class = CustomerSerializer

    # Assignment requires only:
    # Create and List
    http_method_names = [
        "get",
        "post",
        "head",
        "options",
    ]


class OrderViewSet(
    viewsets.ModelViewSet
):

    queryset = (
        Order.objects
        .select_related("customer")
        .prefetch_related(
            "items__product"
        )
        .order_by("-created_at")
    )

    serializer_class = OrderSerializer

    
    http_method_names = [
        "get",
        "post",
        "patch",
        "head",
        "options",
    ]