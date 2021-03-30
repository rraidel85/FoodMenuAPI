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

class Local(models.Model):
    name = models.CharField('Name', max_length=50, unique=True)
    categories = models.ManyToManyField(Category, through='MenuCategory')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Local'
        verbose_name = 'Local'
        verbose_name_plural = 'Locals'
        
class MenuCategory(models.Model):
    local = models.ForeignKey(Local, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.local}->{self.category}'

    class Meta:
        db_table = 'MenuCategory'
        unique_together = ['local', 'category']



def product_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'products/{instance.name}/{filename}'


class Product(models.Model):
    menu_cat = models.ManyToManyField(MenuCategory)
    name = models.CharField('Name', max_length=100, unique=True)
    description = models.CharField('Product Description',blank=True,null=True, max_length=255)
    price = models.DecimalField('Price',max_digits=9, decimal_places=2,default=0.00)
    image = models.ImageField('Image',blank=True,null=True,upload_to=product_image_path)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Comment(models.Model):
    author = models.CharField('Name', max_length=100)
    comment = models.TextField('Comment')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author

    class Meta:
        db_table = 'Comment'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'