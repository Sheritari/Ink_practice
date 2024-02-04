# Generated by Django 5.0.1 on 2024-02-04 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chars_catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='characteristictype',
            options={'verbose_name': 'Виды характеристик', 'verbose_name_plural': 'Виды характеристик'},
        ),
        migrations.AlterField(
            model_name='characteristictype',
            name='json_key_name',
            field=models.CharField(max_length=250, verbose_name='Ключ в json'),
        ),
        migrations.AlterField(
            model_name='characteristictype',
            name='json_value_name',
            field=models.CharField(max_length=250, verbose_name='Значение в json'),
        ),
    ]