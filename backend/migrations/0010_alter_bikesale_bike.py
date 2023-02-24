# Generated by Django 4.1.7 on 2023-02-24 20:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_remove_sale_net_sale_sale_total_sale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bikesale',
            name='bike',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sales', to='backend.bike'),
        ),
    ]
