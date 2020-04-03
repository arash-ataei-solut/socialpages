from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import Profile


class SignupSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(label='password')
    password2 = serializers.CharField(label='password confirm')

    def get_clean_password(self):
        password1 = self.data.get("password1")
        password2 = self.data.get("password2")
        print(password1, password2)
        if not password1 or not password2 or password1 != password2:
            raise serializers.ValidationError(_('passwords must match'))
        return password2

    def create(self, validated_data):
        clean_password = self.get_clean_password()
        if clean_password:
            user, _ = Profile.objects.get_or_create(username=validated_data['username'])
            user.set_password(clean_password)
            user.save()
            return user

    class Meta:
        model = Profile
        fields = ('username', 'password1', 'password2')
        write_only_fields = ('password1', 'password2')


class ProfileDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('username', 'picture', 'first_name', 'last_name', 'email', 'phone', 'birth_date')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Profile
        fields = ('url', 'username', 'picture', 'full_name')
