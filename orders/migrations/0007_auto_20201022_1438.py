# Generated by Django 3.1.2 on 2020-10-22 17:38

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20201022_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='description',
            field=tinymce.models.HTMLField(),
        ),
    ]
