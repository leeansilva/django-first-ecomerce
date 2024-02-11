from django.db import models
from simple_history.models import HistoricalRecords 
from apps.base.models import BaseModel

class MeasureUnit(BaseModel):
    description = models.CharField('Descripción', max_length = 50, unique = True)
    historical = HistoricalRecords()
    
    @property
    def _history_user(self):
        return self.changed_by
    
    #Esto es para que registre que usuario ha realizado el cambio:
    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = "Unidad de medida"
        verbose_name_plural = "Unidades de medida"

    def __str__(self):
        return self.description
    
#*--------------------------------------------------------------------------------------

class CategoryProduct(BaseModel):
    description = models.CharField('Descripción', max_length = 50, unique = True)
    historical = HistoricalRecords()
    
    @property
    def _history_user(self):
        return self.changed_by
    
    #Esto es para que registre que usuario ha realizado el cambio:
    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value
    
    class Meta:
        verbose_name = 'Categoría de producto'
        verbose_name_plural = 'Categorías de producto'

    def __str__(self):
        return self.description

#*--------------------------------------------------------------------------------------

class Indicator(BaseModel):
    
    descount_value = models.PositiveSmallIntegerField(default = 0)
    category_product = models.ForeignKey(CategoryProduct, verbose_name='Indicador de oferta', on_delete=models.CASCADE)
    historical = HistoricalRecords()
    
    @property
    def _history_user(self):
        return self.changed_by
    
    #Esto es para que registre que usuario ha realizado el cambio:
    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value
        
    class Meta:
        verbose_name = 'Indicador de oferta'
        verbose_name_plural = 'Indicadores de oferta'

    def __str__(self):
        return f'Oferta de la categoría {self.category_product} : {self.descount_value}%'

#*--------------------------------------------------------------------------------------

class Product(BaseModel):

    name = models.CharField('Nombre de producto', max_length = 150, unique = True, blank = False, null = False)
    description = models.TextField('Descripción del producto', blank = False, null = False)
    image = models.ImageField('Imágen del producto', upload_to='products/', blank=True, null=True)
    measure_unit = models.ForeignKey(MeasureUnit, verbose_name = 'Unidad de medida', on_delete = models.CASCADE, null = True)
    category_product = models.ForeignKey(CategoryProduct, verbose_name = 'Categoría de producto', on_delete = models.CASCADE, null = True)
    historical = HistoricalRecords()
    
    @property
    def _history_user(self):
        return self.changed_by
    
    #Esto es para que registre que usuario ha realizado el cambio:
    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value
        
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.name

#*--------------------------------------------------------------------------------------


