from rest_framework import serializers

from apps.products.models import Product
from apps.products.api.serializers.general_serializers import MeasureUnitSerializer, CategoryProductSerializer

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        exclude = ('state',)
        
    def to_representation(self, instance):
        return {
            'id' : instance.id,
            'description' : instance.description,
            'image' : instance.image if instance.image != '' else '',
            'measure_unit' : instance.measure_unit.description,
            'category_product' : instance.category_product.description,
        }
        
    def create(self, validated_data):
        if validated_data['image'] == None:
            validated_data['image'] = ''
        return Product.objects.create(**validated_data)