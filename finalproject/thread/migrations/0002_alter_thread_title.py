# Generated by Django 4.2.16 on 2024-10-09 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thread', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
