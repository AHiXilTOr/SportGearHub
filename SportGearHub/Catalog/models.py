from django.db import models

# Create your models here.


class Attribute(models.Model):
    attribute_id = models.AutoField(primary_key=True)
    name = models.ForeignKey('AttributeName', models.DO_NOTHING)
    unit = models.ForeignKey('AttributeUnit', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'attribute'
        verbose_name = 'Атрибут'
        verbose_name_plural = 'Атрибуты'

    def __str__(self):
        return f"{self.name.name} ({self.unit.unit})"


class AttributeName(models.Model):
    attribute_name_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'attribute_name'
        verbose_name = 'Имя атрибута'
        verbose_name_plural = 'Имена атрибутов'

    def __str__(self):
        return self.name


class AttributeUnit(models.Model):
    attribute_unit_id = models.AutoField(primary_key=True)
    unit = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'attribute_unit'
        verbose_name = 'Единица измерения атрибута'
        verbose_name_plural = 'Единицы измерения атрибутов'

    def __str__(self):
        return self.unit


class Brand(models.Model):
    brand_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    country = models.ForeignKey('Country', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'brand'
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Color(models.Model):
    color_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'color'
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'
    
    def __str__(self):
        return self.name


class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    type_of_request = models.ForeignKey('RequestType', models.DO_NOTHING, db_column='type_of_request')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'contact'
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
    
    def __str__(self):
        return f"Тип: {self.type_of_request} (E-mail: {self.email})"


class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'country'
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
    
    def __str__(self):
        return self.name


class Material(models.Model):
    material_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'material'
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'
    
    def __str__(self):
        return self.name

class WarehouseAddress(models.Model):
    warehouse_address_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'warehouse_address'
        verbose_name = 'Адрес склада'
        verbose_name_plural = 'Адреса складов'

    def __str__(self):
        return self.name

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    warranty_months = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    brand = models.ForeignKey(Brand, models.DO_NOTHING)
    category = models.ForeignKey(Category, models.DO_NOTHING)
    material = models.ForeignKey(Material, models.DO_NOTHING)
    colors = models.ManyToManyField(Color, through='ProductColor')
    attributes = models.ManyToManyField(Attribute, through='ProductAttribute')
    warehouses = models.ManyToManyField(WarehouseAddress, through='Warehouse')

    class Meta:
        managed = True
        db_table = 'product'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    product_attribute_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, models.DO_NOTHING)
    attribute = models.ForeignKey(Attribute, models.DO_NOTHING)
    value = models.DecimalField(max_digits=100, decimal_places=2)

    class Meta:
        managed = True
        db_table = 'product_attribute'
        verbose_name = 'Атрибут товара'
        verbose_name_plural = 'Атрибуты товаров'

    def __str__(self):
        return f"{self.product} ({self.attribute} = {self.value})"


class ProductColor(models.Model):
    product_color_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, models.DO_NOTHING)
    color = models.ForeignKey(Color, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'product_color'
        verbose_name = 'Цвет товара'
        verbose_name_plural = 'Цвета товаров'

    def __str__(self):
        return f"{self.product} ({self.color})"


class RequestType(models.Model):
    request_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'request_type'
        verbose_name = 'Имя обращения'
        verbose_name_plural = 'Имена обращений'

    def __str__(self):
        return self.name


class Warehouse(models.Model):
    warehouse_id = models.AutoField(primary_key=True)
    warehouse_address = models.ForeignKey('WarehouseAddress', models.DO_NOTHING)
    product = models.ForeignKey(Product, models.DO_NOTHING)
    quantity = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'warehouse'
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return f"{self.product} - {self.warehouse_address} - {self.quantity}(штук(а))"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, models.DO_NOTHING)
    image = models.ImageField(null=True)

    class Meta:
        managed = True
        db_table = 'product_image'
        verbose_name = 'Фотография товара'
        verbose_name_plural = 'Фотографии товаров'


# class Attribute(models.Model):
#     attribute_id = models.AutoField(primary_key=True)
#     name = models.ForeignKey('AttributeName', models.DO_NOTHING)
#     unit = models.ForeignKey('AttributeUnit', models.DO_NOTHING)

#     class Meta:
#         managed = True
#         db_table = 'attribute'


# class AttributeName(models.Model):
#     attribute_name_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255)

#     class Meta:
#         managed = True
#         db_table = 'attribute_name'


# class AttributeUnit(models.Model):
#     attribute_unit_id = models.AutoField(primary_key=True)
#     unit = models.CharField(max_length=50)

#     class Meta:
#         managed = True
#         db_table = 'attribute_unit'


# class Brand(models.Model):
#     brand_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255)
#     country = models.ForeignKey('Country', models.DO_NOTHING)

#     class Meta:
#         managed = True
#         db_table = 'brand'


# class Category(models.Model):
#     category_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255)

#     class Meta:
#         managed = True
#         db_table = 'category'


# class Color(models.Model):
#     color_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255)

#     class Meta:
#         managed = True
#         db_table = 'color'


# class Contact(models.Model):
#     contact_id = models.AutoField(primary_key=True)
#     type_of_request = models.ForeignKey('RequestType', models.DO_NOTHING, db_column='type_of_request')
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50, blank=True, null=True)
#     email = models.CharField(max_length=50)
#     phone = models.CharField(max_length=20, blank=True, null=True)
#     message = models.CharField(max_length=255)

#     class Meta:
#         managed = True
#         db_table = 'contact'


# class Country(models.Model):
#     country_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255)

#     class Meta:
#         managed = True
#         db_table = 'country'


# class Material(models.Model):
#     material_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255)

#     class Meta:
#         managed = True
#         db_table = 'material'

# class WarehouseAddress(models.Model):
#     warehouse_address_id = models.AutoField(primary_key=True, default=1)
#     name = models.CharField(max_length=255)
#     address = models.CharField(max_length=255)

#     class Meta:
#         managed = True
#         db_table = 'warehouse_address'       

# class Product(models.Model):
#     product_id = models.AutoField(primary_key=True, default=1)
#     name = models.CharField(max_length=255)
#     price = models.DecimalField(max_digits=100, decimal_places=10)
#     warranty_months = models.IntegerField(blank=True, null=True)
#     description = models.TextField(blank=True, null=True)
#     brand = models.ForeignKey(Brand, models.DO_NOTHING)
#     category = models.ForeignKey(Category, models.DO_NOTHING)
#     material = models.ForeignKey(Material, models.DO_NOTHING)
#     attribute = models.ManyToManyField(Attribute)
#     color = models.ManyToManyField(Color)
#     warehouse_address = models.ManyToManyField(WarehouseAddress)

#     class Meta:
#         managed = True
#         db_table = 'product'


# class RequestType(models.Model):
#     request_type_id = models.AutoField(primary_key=True, default=1)
#     name = models.CharField(max_length=50)

#     class Meta:
#         managed = True
#         db_table = 'request_type'

# class ProductImage(models.Model):
#     product = models.ForeignKey(Product, models.DO_NOTHING)
#     image = models.ImageField(null=True)

#     class Meta:
#         managed = True
#         db_table = 'product_image'