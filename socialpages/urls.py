"""socialpages URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from user.views import Signup, Logout, Login


urlpatterns = [
    path('admin/', admin.site.urls),
    path('API/', include_docs_urls(title='Polls API'), name='api'),
    path('api-token/', obtain_jwt_token, name='api-token'),
    path('api-token-refresh/', refresh_jwt_token, name='refresh_token'),
    path('logout/', Logout.as_view(), name='logout'),
    path('login/', Login.as_view(), name='login'),
    path('signup/', Signup.as_view(), name='signup'),
    path('', include('page.urls')),
    path('', include('post.urls')),
    path('', include('user.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
