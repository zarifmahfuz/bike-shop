# Generated by Django 4.1.7 on 2023-02-19 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_alter_bikesale_net_sale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bike',
            name='image',
            field=models.URLField(blank=True, default=''),
            preserve_default=False,
        ),
    ]
