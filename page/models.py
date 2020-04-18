from django.db import models
from django.utils.translation import gettext_lazy as _

from user.models import Profile
from .validators import price_validator


class Page(models.Model):
    owners = models.ManyToManyField(Profile, related_name='page')
    title = models.CharField(_('title'), max_length=255)
    cover = models.ImageField(upload_to='pages', blank=True)
    about = models.TextField(_('about'), max_length=2000, blank=True)
    chasers = models.ManyToManyField(Profile, related_name='chased_pages', blank=True)
    num_chasers = models.DecimalField(max_digits=20, decimal_places=0, default=0)

    price = models.DecimalField(max_digits=10, decimal_places=0, default=0, validators=[price_validator])
    special_users = models.ManyToManyField(
        Profile,
        related_name='special_subscriptions',
        related_query_name='special_subscription',
        blank=True
    )

    class Meta:
        ordering = ('-num_chasers',)

    def __str__(self):
        return self.title
