from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import CategoryView, SubcategoryView, PostView, media_buy

router = SimpleRouter()

router.register('category', CategoryView)
router.register('subcategory', SubcategoryView)
router.register('post', PostView)


urlpatterns = [
    path('media-buy/<int:post_id>/<int:media_id>', media_buy)
] + router.urls
