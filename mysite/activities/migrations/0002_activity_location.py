# Generated by Django 5.1.2 on 2024-11-04 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='location',
            field=models.CharField(default=None, max_length=128),
            preserve_default=False,
        ),
    ]
