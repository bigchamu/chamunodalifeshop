# Generated by Django 3.1.14 on 2023-08-15 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20230815_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featuredproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product', unique=True),
        ),
    ]
