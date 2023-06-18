from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Attribute)
admin.site.register(AttributeName)
admin.site.register(AttributeUnit)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Contact)
admin.site.register(Country)
admin.site.register(Material)
admin.site.register(Product)
admin.site.register(RequestType)
admin.site.register(WarehouseAddress)
admin.site.register(ProductImage)

# Много-ко-многим
admin.site.register(ProductAttribute)
admin.site.register(ProductColor)
admin.site.register(Warehouse)