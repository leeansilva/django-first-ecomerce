
from apps.base.api import GeneralListAPIView
from apps.products.api.serializers.general_serializers import MeasureUnitSerializer, IndicatorSerializer, CategoryProductSerializer

#Aqui lo que hacemos es heredar de GeralListAPIView los metodos de get, y la serializer_class para evitar codigo repetitivo. 
class MeasureUnitListAPIView(GeneralListAPIView):
    #ListAPIView es para consultas tipo listas, osea muchos objetos
    serializer_class = MeasureUnitSerializer
class IndicatorListAPIView(GeneralListAPIView):
    #ListAPIView es para consultas tipo listas, osea muchos objetos
    serializer_class = IndicatorSerializer

class CategoryProductListAPIView(GeneralListAPIView):
    #ListAPIView es para consultas tipo listas, osea muchos objetos
    serializer_class = CategoryProductSerializer
    
        
    
    
