from rest_framework import viewsets
from app.models import Product,OrderPlaced
from app.Api.serilizers import ProductSerializer,OrderPlacedSerializer

class ProductApi(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class OrderPlacedApi(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderPlacedSerializer
    queryset = OrderPlaced.objects.all()
