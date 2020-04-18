from hurry.filesize import size
from django.db import models
from django.core.validators import FileExtensionValidator

from page.models import Page
from user.models import Profile
from .validators import validate_file_size, price_validator


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    chasers = models.ManyToManyField(Profile, related_name='chased_categories', blank=True)
    num_chasers = models.DecimalField(max_digits=20, decimal_places=0, default=0)

    class Meta:
        ordering = ('-num_chasers',)
        indexes = [
            models.Index(fields=['name', 'id'])
        ]

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    chasers = models.ManyToManyField(Profile, related_name='chased_subcategories', blank=True)
    num_chasers = models.DecimalField(max_digits=20, decimal_places=0, default=0)

    class Meta:
        ordering = ('-num_chasers',)
        indexes = [
            models.Index(fields=['name', 'id'])
        ]

    def __str__(self):
        return self.category.name + ' - ' + self.name


def user_directory_path(instance, filename):
    return 'sender_{0}/{1}'.format(instance.sender.username, filename)


class Post(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='post')
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='post')

    subcategories = models.ManyToManyField(Subcategory, related_name='post')
    title = models.CharField(max_length=255)
    cover = models.ImageField(upload_to=user_directory_path)
    caption = models.TextField(max_length=5000, blank=True)

    viewed_by = models.ManyToManyField(Profile, related_name='viewed_posts', blank=True)

    create_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)

    price = models.DecimalField(max_digits=10, decimal_places=0, default=0, validators=[price_validator])
    special_users = models.ManyToManyField(
        Profile,
        related_name='bought_posts',
        related_query_name='bought_post',
        blank=True
    )

    class Meta:
        ordering = ('-create_date',)

    def __str__(self):
        return self.title


class MediaFile(models.Model):
    file = models.FileField(
        upload_to='files',
        validators=[FileExtensionValidator(['pdf', 'jpg', 'png', 'mp3', 'mp4', 'mkv']), validate_file_size],
        blank=True
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='medias')
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0, validators=[price_validator])
    special_users = models.ManyToManyField(
        Profile,
        related_name='bought_medias',
        related_query_name='bought_media',
        blank=True
    )

    def file_size(self):
        return size(self.file.size)

    @property
    def is_special(self):
        return False if self.price == 0 else True


class Rate(models.Model):
    rate = models.DecimalField(max_digits=2, decimal_places=2, default=0.99)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='rates')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='rates')

    class Meta:
        unique_together = ('user', 'post')
