# Generated by Django 3.0.4 on 2020-04-03 10:50

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import post.models
import post.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('page', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('num_chasers', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('chasers', models.ManyToManyField(blank=True, related_name='chased_categories', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-num_chasers',),
            },
        ),
        migrations.CreateModel(
            name='MediaFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to='files', validators=[django.core.validators.FileExtensionValidator(['pdf', 'jpg', 'png', 'mp3', 'mp4', 'mkv']), post.validators.validate_file_size])),
                ('price', models.DecimalField(decimal_places=0, default=0, max_digits=10, validators=[post.validators.price_validator])),
                ('special_users', models.ManyToManyField(blank=True, related_name='bought_medias', related_query_name='bought_media', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('cover', models.ImageField(upload_to=post.models.user_directory_path)),
                ('caption', models.TextField(blank=True, max_length=5000)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('edit_date', models.DateTimeField(auto_now=True)),
                ('price', models.DecimalField(decimal_places=0, default=0, max_digits=10, validators=[post.validators.price_validator])),
                ('medias', models.ManyToManyField(blank=True, related_name='post', to='post.MediaFile')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to=settings.AUTH_USER_MODEL)),
                ('special_users', models.ManyToManyField(blank=True, related_name='bought_posts', related_query_name='bought_post', to=settings.AUTH_USER_MODEL)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='page.Page')),
            ],
            options={
                'ordering': ('-create_date',),
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('num_chasers', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='post.Category')),
                ('chasers', models.ManyToManyField(blank=True, related_name='chased_subcategories', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-num_chasers',),
            },
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.DecimalField(decimal_places=2, default=0.99, max_digits=2)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates', to='post.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='subcategories',
            field=models.ManyToManyField(related_name='post', to='post.Subcategory'),
        ),
        migrations.AddField(
            model_name='post',
            name='viewed_by',
            field=models.ManyToManyField(blank=True, related_name='viewed_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='subcategory',
            index=models.Index(fields=['name', 'id'], name='post_subcat_name_159506_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='rate',
            unique_together={('user', 'post')},
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['name', 'id'], name='post_catego_name_29de53_idx'),
        ),
    ]
