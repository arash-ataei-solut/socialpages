from rest_framework import serializers

from .models import Post, Subcategory, Category, MediaFile, Rate
from page.serializers import PageSerializer
from user.serializers import ProfileSerializer


class SubcategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Subcategory
        fields = ['url', 'id', 'name', 'num_chasers']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    subcategories = SubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['url', 'id', 'name', 'num_chasers', 'subcategories']


class SubcategoryDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    chasers = ProfileSerializer(many=True)

    class Meta:
        model = Subcategory
        fields = ['name', 'id', 'category', 'chasers', 'num_chasers']


class SubcategoryCreateSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField

    class Meta:
        model = Subcategory
        fields = ['name', 'id', 'category']


class CategoryDetailSerializer(serializers.ModelSerializer):
    chasers = ProfileSerializer(many=True)

    class Meta:
        model = Category
        fields = ['name', 'id', 'chasers', 'num_chasers']


class CategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['name', 'id']


class HideMediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = MediaFile
        fields = ['id', 'price', 'file_size']


class MediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = MediaFile
        fields = ['id', 'file_size', 'file', 'price']


class PostSerializer(serializers.HyperlinkedModelSerializer):
    sender = ProfileSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['url', 'id', 'sender', 'title', 'cover']


class PostDetailSerializer(serializers.ModelSerializer):
    page = PageSerializer()
    sender = ProfileSerializer(read_only=True)
    subcategories = SubcategorySerializer(many=True)
    viewed_by = ProfileSerializer(many=True)
    views = serializers.SerializerMethodField()
    special_users = ProfileSerializer(many=True)

    def get_views(self, post):
        return post.viewed_by.all().count()

    class Meta:
        model = Post
        fields = [
            'id',
            'page',
            'sender',
            'title',
            'caption',
            'subcategories',
            'viewed_by',
            'views',
            'price',
            'special_users',
        ]


class PostCreateSerializer(serializers.ModelSerializer):
    subcategories = serializers.StringRelatedField

    def get_views(self, post):
        return post.viewed_by.all().count()

    class Meta:
        model = Post
        fields = [
            'title',
            'caption',
            'subcategories',
            'price',
        ]


class RateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rate
        fields = ['rate']
