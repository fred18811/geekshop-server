# Generated by Django 3.2.4 on 2021-08-09 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='quantitly',
            new_name='quantity',
        ),
    ]
