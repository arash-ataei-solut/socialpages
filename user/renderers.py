from rest_framework import renderers


class UserRenderer(renderers.BrowsableAPIRenderer):
    template = 'user.html'


class SignupRenderer(renderers.BrowsableAPIRenderer):
    template = 'signup.html'


class LoginRenderer(renderers.BrowsableAPIRenderer):
    template = 'login.html'
