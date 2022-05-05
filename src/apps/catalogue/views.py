from rest_framework import viewsets
from rest_framework import mixins
from catalogue import serializers
from catalogue import models


class ProductViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
