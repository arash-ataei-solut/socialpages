# Generated by Django 3.0.5 on 2020-05-06 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0009_auto_20200507_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='edit_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]