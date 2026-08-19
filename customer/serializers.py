from decimal import Decimal

from django.db import transaction

from rest_framework import serializers

from .models import (
    Product,
    Customer,
    Order,
    OrderItem
)


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"

    def validate_price(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than 0."
            )

        return value


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem

        fields = [
            "id",
            "product",
            "quantity",
            "price",
            "subtotal",
        ]

        read_only_fields = [
            "id",
            "price",
            "subtotal",
        ]


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(
        many=True
    )

    class Meta:
        model = Order

        fields = [
            "id",
            "customer",
            "status",
            "total",
            "items",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "total",
            "created_at",
            "updated_at",
        ]

    def validate_items(self, items):

        if not items:
            raise serializers.ValidationError(
                "Order must contain at least one item."
            )

        product_ids = [
            item["product"].id
            for item in items
        ]

        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError(
                "Same product cannot be added twice."
            )

        return items

    def create(self, validated_data):

        items_data = validated_data.pop(
            "items"
        )

        with transaction.atomic():

            order = Order.objects.create(
                customer=validated_data["customer"]
            )

            total = Decimal("0.00")

            for item_data in items_data:

                product = (
                    Product.objects
                    .select_for_update()
                    .get(
                        id=item_data["product"].id
                    )
                )

                quantity = item_data["quantity"]

                if quantity <= 0:
                    raise serializers.ValidationError(
                        "Quantity must be greater than 0."
                    )

                if product.stock < quantity:

                    raise serializers.ValidationError(
                        f"Not enough stock for "
                        f"{product.name}. "
                        f"Available stock: "
                        f"{product.stock}"
                    )

                # Price comes from database
                price = product.price

                subtotal = price * quantity

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price,
                    subtotal=subtotal
                )

                # Reduce stock
                product.stock -= quantity
                product.save()

                total += subtotal

            # Backend calculates total
            order.total = total
            order.save()

        return order

    def update(self, instance, validated_data):

        new_status = validated_data.get(
            "status",
            instance.status
        )

        # Check if order is being cancelled
        if (
            instance.status != Order.Status.CANCELLED
            and new_status == Order.Status.CANCELLED
        ):

            with transaction.atomic():

                for item in instance.items.all():

                    product = item.product

                    product.stock += item.quantity

                    product.save()

                instance.status = Order.Status.CANCELLED

                instance.save()

            return instance

        # For any other update
        return super().update(
            instance,
            validated_data
        )