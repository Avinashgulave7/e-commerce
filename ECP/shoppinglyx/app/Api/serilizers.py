from rest_framework.serializers import ModelSerializer
from app.models import Product,OrderPlaced

class ProductSerializer(ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'


class OrderPlacedSerializer(ModelSerializer):
    class Meta:
        model=OrderPlaced
        fields='__all__'