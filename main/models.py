from django.db import models
from django.utils.text import slugify

class Category(models.Model): #Категоря товара "майка, шорты и т.д."
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True) #slug нужен для подставления URL


    def save(self, *args, **kwargs): #Если мы не пишем категорию, эта функция
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs) #С помощью супер-метода присваевает значения сама
    


    def __str__(self): #Способ отображения в админке
        return self.name
    

class Size(models.Model):
    name = models.CharField(max_length=20)


    def __str__(self):
        return self.name
    

class ProductSize(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE,
                                related_name='product_size')
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)


    def __str__(self):
        return f"{self.size.name} ({self.stock} in stock) for {self.product.name}"
                 #Размер М          20шт на складе            для черной футболки 


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, 
                                 related_name='products') #ForeignKey наследует поля из других моделей
    color = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    main_immage = models.ImageField(upload_to='products/main/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs): 
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name

class ProductImage(models.Model):  #Второстипенные картинки товара
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='images')
    image = models.ImageField(upload_to='product/extra/')

