from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import (RefreshToken)
from .models import (Product,Customer)

class InventoryAPITestCase(APITestCase):

    def setUp(self):
        user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=(f"Bearer {access_token}"))
        self.customer = Customer.objects.create(name="Test Customer",email="test@example.com",phone="9999999999")
        self.product = Product.objects.create(name="Keyboard",sku="KB001",price=1000,stock=10)

    def test_product_sku_unique(self):

        response = self.client.post("/api/products/",
            {
                "name": "Another Keyboard",
                "sku": "KB001",
                "price": 1200,
                "stock": 5
            },format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_order_reduces_stock(self):

        response = self.client.post(
            "/api/orders/",
            {
                "customer": self.customer.id,
                "items": [
                    {
                        "product": self.product.id,
                        "quantity": 3
                    }
                ]
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.stock,
            7
        )

    def test_insufficient_stock(self):

        response = self.client.post(
            "/api/orders/",
            {
                "customer": self.customer.id,
                "items": [
                    {
                        "product": self.product.id,
                        "quantity": 20
                    }
                ]
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.stock,
            10
        )

    def test_backend_calculates_total(self):

        response = self.client.post(
            "/api/orders/",
            {
                "customer": self.customer.id,
                "items": [
                    {
                        "product": self.product.id,
                        "quantity": 2
                    }
                ]
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.data["total"],
            "2000.00"
        )

    def test_cancel_restores_stock(self):

        response = self.client.post(
            "/api/orders/",
            {
                "customer": self.customer.id,
                "items": [
                    {
                        "product": self.product.id,
                        "quantity": 3
                    }
                ]
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        order_id = response.data["id"]

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.stock,
            7
        )

        response = self.client.patch(
            f"/api/orders/{order_id}/",
            {
                "status": "CANCELLED"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.stock,
            10
        )