# Generated by Django 3.0.5 on 2020-06-04 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
        ('products', '0001_initial'),
        ('packages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('price', models.IntegerField()),
                ('day', models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3')], max_length=1, null=True)),
                ('leg', models.CharField(blank=True, choices=[('1', '1'), ('2', '2')], max_length=1, null=True)),
                ('shoulder', models.CharField(blank=True, choices=[('1', '1'), ('2', '2')], max_length=1, null=True)),
                ('discount', models.IntegerField(default=0, null=True)),
                ('complete', models.BooleanField(default=False)),
                ('processing', models.BooleanField(default=False)),
                ('ready', models.BooleanField(default=False)),
                ('delivered', models.BooleanField(default=False)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.Category')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='orders.Order')),
                ('package', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='packages.Package')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='products.Product')),
                ('time', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='order_items.Time')),
            ],
        ),
    ]
