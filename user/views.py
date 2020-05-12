from datetime import datetime, timedelta
import smtplib

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.views import ObtainJSONWebToken

from rest_framework_jwt.settings import api_settings

from . import serializers as se
from .models import Profile
from post.renderers import MyRenderer
from .renderers import UserRenderer, SignupRenderer, LoginRenderer


class Signup(APIView):
    serializer_class = se.SignupSerializer
    renderer_classes = [JSONRenderer, SignupRenderer]

    def get(self, request):
        if request.user.is_authenticated:
            return Response({'you': request.user.username})
        else:
            return Response({'status': 'signing up'})

    def post(self, request):
        serializer = se.SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = Profile.objects.create(username=serializer.data['username'], email=serializer.data['email'])
            user.set_password(serializer.data['password2'])
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            account_activation_token = PasswordResetTokenGenerator()
            message = render_to_string('email_template.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login("arash.ataee76@yahoo.com", "man2Setdaram")
            to_email = serializer.data.get('email')
            text = message
            server.sendmail('arash.ataee76@yahoo.com', to_email, text)
            return Response('Please confirm your email address to complete the registration')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view()
def activate(request, uidb64, token):
    account_activation_token = PasswordResetTokenGenerator()
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return Response('Thank you for your email confirmation. Now you can login your account.')
    else:
        return Response('Activation link is invalid!')


class LoginView(ObtainJSONWebToken):
    renderer_classes = [JSONRenderer, LoginRenderer]

    def get(self, request):
        return Response('login')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            last_url = request.last_url
        except AttributeError:
            last_url = '/'

        if serializer.is_valid():
            print(serializer.object.get('token'))
            token = serializer.object.get('token')
            response = HttpResponseRedirect(last_url)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):

    def post(self, request):
        response = HttpResponseRedirect(request.data['last_url'])
        response.delete_cookie('Authorization', path='/')
        return response


class MyProfileView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializers = {
        'retrieve': se.MyProfileDetailSerializer,
        'update': se.MyProfileUpdateSerializer,
        'destroy': se.MyProfileUpdateSerializer
    }

    def get_queryset(self):
        return self.request.user


class ProfileView(ReadOnlyModelViewSet):
    queryset = Profile.objects.all()

    serializers = {
        'list': se.ProfileSerializer,
        'retrieve': se.ProfileDetailSerializer
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action)
