# Generated by Django 3.1.5 on 2021-05-24 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210425_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='timestamp',
            field=models.CharField(default='0', max_length=25),
            preserve_default=False,
        ),
    ]