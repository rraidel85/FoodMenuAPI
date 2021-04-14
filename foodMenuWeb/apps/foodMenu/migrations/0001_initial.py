# Generated by Django 3.1.7 on 2021-03-30 07:43

from django.db import migrations, models
import django.db.models.deletion
import foodMenuWeb.apps.foodMenu.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'db_table': 'Category',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=100, verbose_name='Name')),
                ('comment', models.TextField(verbose_name='Comment')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'db_table': 'Comment',
            },
        ),
        migrations.CreateModel(
            name='Local',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Local',
                'verbose_name_plural': 'Locals',
                'db_table': 'Local',
            },
        ),
        migrations.CreateModel(
            name='MenuCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodMenu.category')),
                ('local', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodMenu.local')),
            ],
            options={
                'db_table': 'MenuCategory',
                'unique_together': {('local', 'category')},
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Product Description')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Price')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='Image')),
                ('menu_cat', models.ManyToManyField(to='foodMenu.MenuCategory')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'db_table': 'Product',
            },
        ),
        migrations.AddField(
            model_name='local',
            name='categories',
            field=models.ManyToManyField(through='foodMenu.MenuCategory', to='foodMenu.Category'),
        ),
    ]
