# Generated by Django 3.1.7 on 2021-04-14 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodMenu', '0006_auto_20210331_1747'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='menu_cat',
        ),
        migrations.AddField(
            model_name='menucategory',
            name='products',
            field=models.ManyToManyField(related_name='menus', to='foodMenu.Product'),
        ),
    ]
