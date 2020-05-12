from django.contrib.auth.password_validation import validate_password, MinimumLengthValidator
from django.core import exceptions
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer

from .models import Profile
from .validators import UppercasePasswordValidator, HasDigitPasswordValidator


class SignupSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        label='password',
        style={'input_type': 'password'},
        validators=[validate_password, UppercasePasswordValidator(), HasDigitPasswordValidator()]
    )
    password2 = serializers.CharField(label='password confirm', style={'input_type': 'password'})

    def validate_password2(self, value):
        password1 = self.initial_data.get("password1")
        password2 = self.initial_data.get("password2")
        if password1 != password2:
            raise serializers.ValidationError('passwords must match')
        return value

    class Meta:
        model = Profile
        fields = ('username', 'email', 'password1', 'password2')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('url', 'id', 'username', 'picture', 'full_name')


class ProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'id',
            'username',
            'picture',
            'first_name',
            'last_name',
            'email',
            'phone',
            'birth_date'
        )


from post import serializers as post_se
from page import serializers as page_se


class MyProfileDetailSerializer(serializers.ModelSerializer):
    chased_pages = page_se.PageSerializer(many=True)
    chased_categories = post_se.CategorySerializer(many=True)
    chased_subcategories = post_se.SubcategorySerializer(many=True)

    class Meta:
        model = Profile
        fields = (
            'id',
            'username',
            'picture',
            'budget',
            'first_name',
            'last_name',
            'email',
            'phone',
            'birth_date',
            'is_active',
            'chased_pages',
            'chased_categories',
            'chased_subcategories',
        )


class MyProfileUpdateSerializer(serializers.ModelSerializer):
    chased_pages = serializers.StringRelatedField
    chased_categories = serializers.StringRelatedField
    chased_subcategories = serializers.StringRelatedField

    class Meta:
        model = Profile
        fields = (
            'id',
            'username',
            'picture',
            'first_name',
            'last_name',
            'email',
            'phone',
            'birth_date',
            'chased_pages',
            'chased_categories',
            'chased_subcategories',
        )
