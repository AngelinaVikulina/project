# Generated by Django 4.2.16 on 2024-10-15 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='stock',
            field=models.PositiveIntegerField(default=10),
        ),
    ]