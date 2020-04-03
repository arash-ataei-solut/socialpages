from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.db import transaction

from .models import Page
from user.models import Profile


@shared_task
def buy(username, pk):
    with transaction.atomic():
        user = Profile.objects.select_for_update().filter(username=username)[0]
        page = Page.objects.select_for_update().filter(pk=pk).prefetch_related('special_users')[0]
        if user not in page.special_users.all() and user.budget >= page.price:
            user.budget = user.budget - page.price
            page.special_users.add(user)
            user.save()
            page.save()
