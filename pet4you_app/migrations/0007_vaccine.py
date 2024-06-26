# Generated by Django 5.0.4 on 2024-06-19 21:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet4you_app', '0006_alter_pet_favorited'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vaccine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('next_due_date', models.DateField(blank=True, null=True)),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vaccines', to='pet4you_app.pet')),
            ],
        ),
    ]
