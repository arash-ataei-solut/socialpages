from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import PageView

router = SimpleRouter()

router.register('page', PageView)


urlpatterns = [

] + router.urls
