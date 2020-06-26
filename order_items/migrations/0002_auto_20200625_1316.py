# Generated by Django 3.0.5 on 2020-06-25 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_items', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='leg',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='shoulder',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
    ]
