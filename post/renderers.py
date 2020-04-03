from rest_framework import renderers


class MyRenderer(renderers.BrowsableAPIRenderer):
    template = 'index.html'

