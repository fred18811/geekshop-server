# Generated by Django 3.2.4 on 2021-07-29 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210729_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=128, unique=True),
        ),
    ]
