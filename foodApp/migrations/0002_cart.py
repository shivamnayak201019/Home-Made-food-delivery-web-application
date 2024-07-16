# Generated by Django 5.0.4 on 2024-06-19 15:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('amountPerQuantity', models.FloatField()),
                ('custCartForeign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodApp.customers1')),
                ('foodUploadForeign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodApp.foodupload')),
            ],
            options={
                'db_table': 'cart',
            },
        ),
    ]
