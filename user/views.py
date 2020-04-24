from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.utils import jwt_response_payload_handler
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

import jwt
from rest_framework_jwt.settings import api_settings

from . import serializers as se
from .models import Profile

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


def get_user_by_token(request):
    token = request.COOKIES['Authorization']

    try:
        payload = jwt_decode_handler(token)
    except jwt.ExpiredSignature:
        return
    except jwt.DecodeError:
        return

    username = jwt_get_username_from_payload(payload)
    return username


class Signup(APIView):
    serializer_class = se.SignupSerializer

    def get(self, request):
        if request.user.is_authenticated:
            return Response({'you': request.user.username})
        else:
            return Response({'status': 'signing up'})

    def post(self, request):
        serializer = se.SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'you signed up successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(ObtainJSONWebToken):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            token = serializer.object.get('token')
            response = HttpResponseRedirect(request.data['the url'])
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):

    def post(self, request):
        response = HttpResponseRedirect(request.data['the url'])
        response.delete_cookie('Authorization', path='/')
        return response


class ProfileView(APIView):
    serializer_class = se.ProfileDetailSerializer

    def get(self, request):
        user = Profile.objects.get(username=get_user_by_token(request))
        return Response(se.ProfileDetailSerializer(user).data)

    def put(self, request):
        user = Profile.objects.get(username=get_user_by_token(request))
        serializer = se.ProfileDetailSerializer(user)
        serializer.update(validated_data=request.data, instance=user)
        return Response({'status': 'you signed up successfully'})


class ProfileViewSet(ReadOnlyModelViewSet):
    queryset = Profile.objects.all()

    serializers = {
        'list': se.ProfileSerializer,
        'retrieve': se.ProfileDetailSerializer
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action)
