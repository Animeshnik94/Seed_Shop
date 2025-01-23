from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название категории')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    image = models.ImageField(upload_to='categories_images', blank=True, null=True, verbose_name='Иконка категории')

    class Meta:
        db_table = 'category'
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
        ordering = ("id",)

    def __str__(self):
        return self.name

class Grower(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Производитель')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table = 'grower'
        verbose_name = 'Производителя'
        verbose_name_plural = 'Производители'
        ordering = ("id",)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название продукта')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='goods_images', blank=True, null=True, verbose_name='Изображение')
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, verbose_name='Скидка в %')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    flowering_time = models.PositiveIntegerField(default=0, verbose_name='Длительность (дни)')
    sativa_share = models.PositiveIntegerField(default=0, verbose_name='Доля сативы (%)')
    indica_share = models.PositiveIntegerField(default=0, verbose_name='Доля индики (%)')
    thc = models.PositiveIntegerField(default=0, verbose_name='ТГК (%)') 
    # Внешние ключи 
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name='Категория')
    grower = models.ForeignKey(to=Grower, on_delete=models.CASCADE, verbose_name='Производитель')
    # Внешний ключ. FK categories. PROTECT-если все связанные товары не удалены, удалить категорию невозможно
    #CASCADE- при удалении категории удалятся и все связанные товары
    #SET_DEFAULT(something)- в поле категория товаров будет указано значение по умолчанию 

    class Meta:
        db_table = 'product'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'{self.name} Количество - {self.quantity}'
    
    def display_id(self):
        return f'{self.id:05}'
    
    def sell_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)
        return self.price 
    
    def save(self, *args, **kwargs):
        self.indica_share = 100 - self.sativa_share
        super().save(*args, **kwargs)