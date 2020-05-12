from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import ProfileView, activate

router = SimpleRouter()
router.register('profiles', ProfileView)

urlpatterns = [
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate')
] + router.urls
