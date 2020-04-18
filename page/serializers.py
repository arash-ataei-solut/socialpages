from rest_framework import serializers

from .models import Page
from user.serializers import ProfileSerializer


class PageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Page
        fields = ['url', 'title', 'cover', 'num_chasers']


class PageDetailSerializer(serializers.ModelSerializer):
    owners = ProfileSerializer(many=True)

    class Meta:
        model = Page
        fields = ['owners', 'title', 'cover', 'about', 'chasers', 'num_chasers', 'price']


class PageCreateSerializer(serializers.ModelSerializer):
    owners = serializers.StringRelatedField

    class Meta:
        model = Page
        fields = ['owners', 'title', 'cover', 'about', 'price']
