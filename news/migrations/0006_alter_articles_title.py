# Generated by Django 4.2.16 on 2024-10-20 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_comment_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='title',
            field=models.CharField(max_length=50, verbose_name='Заголовок'),
        ),
    ]
