# Generated by Django 5.0.4 on 2024-04-28 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet4you_app', '0004_pet_favorited'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='photo',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
