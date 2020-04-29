from rest_framework.pagination import PageNumberPagination


class MyPagination(PageNumberPagination):
    template = 'number.html'
