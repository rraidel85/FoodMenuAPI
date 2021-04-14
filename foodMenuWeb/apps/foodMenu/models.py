from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField('Name', max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['id']

class Local(models.Model):
    name = models.CharField('Name', max_length=50, unique=True)
    categories = models.ManyToManyField(Category, through='MenuCategory', related_name='locals')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Local'
        verbose_name = 'Local'
        verbose_name_plural = 'Locals'
        ordering = ['id']


class Product(models.Model):
    name = models.CharField('Name', max_length=100, unique=True)
    description = models.CharField('Product Description',blank=True,null=True, max_length=255)
    price = models.DecimalField('Price',max_digits=9, decimal_places=2)
    image = models.ImageField('Image',blank=True,null=True,upload_to='products/')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['id']


class Comment(models.Model):
    author = models.CharField('Author', max_length=100)
    comment = models.TextField('Comment')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author

    class Meta:
        db_table = 'Comment'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['id']


class MenuCategory(models.Model):
    local = models.ForeignKey(Local, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='menus')

    def __str__(self):
        return f'{self.local}->{self.category}'

    class Meta:
        db_table = 'MenuCategory'
        unique_together = ['local', 'category']
        ordering = ['id']
