# Generated by Django 3.0.5 on 2020-05-06 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0011_auto_20200506_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='create_date',
            field=models.TimeField(),
        ),
    ]