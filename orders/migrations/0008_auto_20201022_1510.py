# Generated by Django 3.1.2 on 2020-10-22 18:10

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20201022_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
    ]