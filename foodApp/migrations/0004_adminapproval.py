# Generated by Django 5.0.4 on 2024-07-04 03:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodApp', '0003_cart_totalamount'),
    ]

    operations = [
        migrations.CreateModel(
            name='adminApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approval', models.BooleanField(default=False, verbose_name='Approve')),
                ('foodUploadChef', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodApp.foodupload')),
            ],
        ),
    ]
