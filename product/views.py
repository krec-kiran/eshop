from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .filters import ProductFilter
from rest_framework.pagination import PageNumberPagination

from .models import Product
from .serializers import ProductSerializer

# Create your views here.

@api_view(['GET'])
def get_products(request):
    filterset = ProductFilter(request.GET,queryset=Product.objects.all().order_by('id'))
    count = filterset.qs.count()
    # Pagination
    resPerPage = 1
    paginator = PageNumberPagination()
    paginator.page_size = resPerPage
    queryset = paginator.paginate_queryset(filterset.qs,request)
    # products = Product.objects.all()
    serializer = ProductSerializer(queryset,many=True)    
    return Response({
        "count": count,
        "res_per_page": resPerPage,        
        "products": serializer.data})

@api_view(['GET'])
def get_product(request,pk):
    product = get_object_or_404(Product,id=pk)
    serializer = ProductSerializer(product,many=False)
    return Response({"product": serializer.data})

    
    
    
