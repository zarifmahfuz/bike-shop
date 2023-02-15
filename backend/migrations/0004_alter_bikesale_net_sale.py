# Generated by Django 4.1.6 on 2023-02-15 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_remove_sale_created_at_sale_sold_at_sale_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bikesale',
            name='net_sale',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='net_sale = sale value - discount applied'),
        ),
    ]
