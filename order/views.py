from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from rest_framework import status

from .serializers import OrderSerializer

from product.models import Product
from rest_framework.pagination import PageNumberPagination

from .models import Order, OrderItem

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders,many = True)
    return Response({'orders':serializer.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order(request, pk):
    order = get_object_or_404(Order, id=pk)

    serializer = OrderSerializer(order, many=False)

    return Response({'order': serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_order(request):

    user = request.user
    data = request.data

    order_items = data['orderItems']

    if order_items and len(order_items) == 0:
        return Response({ 'error': 'No Order Items. Please add atleast one product' }, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Create order

        total_amount = sum(item['price'] * item['quantity'] for item in order_items)

        order = Order.objects.create(
            user=user,
            street=data['street'],
            city=data['city'],
            state=data['state'],
            zip_code=data['zip_code'],
            phone_no=data['phone_no'],
            country=data['country'],
            total_amount=total_amount
        )

        # Create order items and set order to order items 
        for i in order_items:
            product = Product.objects.get(id=i['product'])
            if product.stock < i['quantity']:
                 return Response({'error': 'No sufficient stock of this product to place an order'})
            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                quantity = i['quantity'],
                price = i['price']
            )

            # Update product stock
            product.stock -= item.quantity
            product.save()


        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def process_order(request, pk):
    order = get_object_or_404(Order, id=pk)

    order.status = request.data['status']

    order.save()

    serializer = OrderSerializer(order, many=False)

    return Response({'order': serializer.data})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_order(request, pk):
    order = get_object_or_404(Order, id=pk)

    order.delete()


    return Response({'details': 'Order is deleted.'})
