from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import CategoryView, SubcategoryView, PostView, buy_media, LastDayView, rate_post_view, comment_post_view


router = SimpleRouter()

router.register('category', CategoryView)
router.register('subcategory', SubcategoryView)
router.register('post', PostView)


urlpatterns = [
    path('buy-media/<int:post_id>/<int:media_id>/', buy_media),
    path('rate/<int:pk>/', rate_post_view, name='rate'),
    path('comment/<int:pk>/', comment_post_view, name='comment'),
    path('', LastDayView.as_view(), name='24h')
] + router.urls
