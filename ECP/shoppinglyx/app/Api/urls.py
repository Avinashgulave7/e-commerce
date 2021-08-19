from django.urls import path,include
from rest_framework import routers
from app.Api.views import ProductApi,OrderPlacedApi
router=routers.DefaultRouter()

router.register('product',ProductApi)
router.register('orderplaced',OrderPlacedApi)

urlpatterns = [
path('', include(router.urls)),


]