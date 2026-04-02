from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.
class Producto(models.Model):
    productoId = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    unidades_stock = models.IntegerField(validators=[MinValueValidator(0)])
    
    class Meta:
        db_table = "producto"

    def __str__(self):
        return self.nombre_producto 