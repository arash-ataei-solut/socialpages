from django.db.models import Avg, F
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from collections import OrderedDict

from user.models import Profile
from .models import Post, Subcategory, Category, MediaFile
from . import serializers as se
from .tasks import rate, buy, buy_media
from .renderers import MyRenderer
from .permissions import IsSenderOrIsAuthenticatedOrReadOnly
from user.views import get_user_by_token


class CategoryView(GenericViewSet, ListModelMixin, CreateModelMixin):
    renderer_classes = [JSONRenderer, MyRenderer]
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

    serializers = {
        'list': se.CategorySerializer,
        'retrieve': se.PostSerializer,
        'create': se.CategoryCreateSerializer
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action)

    def retrieve(self, request, **kwargs):
        category = Category.objects.get(pk=kwargs['pk'])
        category_info = se.CategoryDetailSerializer(category, context={'request': request})

        qs = Post.objects.filter(
            subcategories__category=category
        ).annotate(
            average_rate=Avg('rates__rate')
        ).order_by(
            F('average_rate').desc(nulls_first=True), '-create_date'
        )

        queryset = SearchFilter().filter_queryset(
            self.request,
            qs,
            PostView()
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response(OrderedDict([
                ('count', self.paginator.page.paginator.count),
                ('next', self.paginator.get_next_link()),
                ('previous', self.paginator.get_previous_link()),
                ('category_info', category_info.data),
                ('results', serializer.data),
            ]))

        serializer = self.get_serializer(queryset, many=True)
        return Response(OrderedDict([
            ('category_info', category_info.data),
            ('post', serializer.data),
        ]))


class SubcategoryView(GenericViewSet, ListModelMixin, CreateModelMixin):
    renderer_classes = [JSONRenderer, MyRenderer]
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Subcategory.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

    serializers = {
        'list': se.SubcategorySerializer,
        'retrieve': se.PostSerializer,
        'create': se.SubcategoryCreateSerializer
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action)

    def retrieve(self, request, **kwargs):
        subcategory = Subcategory.objects.get(pk=kwargs['pk'])
        subcategory_info = se.CategoryDetailSerializer(subcategory, context={'request': request})

        qs = Post.objects.filter(
            subcategories=subcategory
        ).annotate(
            average_rate=Avg('rates__rate')
        ).order_by(
            F('average_rate').desc(nulls_first=True), '-create_date'
        )

        queryset = SearchFilter().filter_queryset(
            request,
            qs,
            PostView()
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response(OrderedDict([
                ('count', self.paginator.page.paginator.count),
                ('next', self.paginator.get_next_link()),
                ('previous', self.paginator.get_previous_link()),
                ('category_info', subcategory_info.data),
                ('results', serializer.data),
            ]))

        serializer = self.get_serializer(queryset, many=True)
        return Response(OrderedDict([
            ('category_info', subcategory_info.data),
            ('post', serializer.data),
        ]))


class PostView(GenericViewSet, ListModelMixin, UpdateModelMixin):
    renderer_classes = [JSONRenderer, MyRenderer]
    permission_classes = [IsSenderOrIsAuthenticatedOrReadOnly]
    queryset = qs = Post.objects.all().annotate(
        average_rate=Avg('rates__rate')
    ).order_by(
        F('average_rate').desc(nulls_first=True), '-create_date'
    )
    filter_backends = (SearchFilter,)
    search_fields = ('title',)

    serializers = {
        'list': se.PostSerializer,
        'retrieve': se.PostDetailSerializer,
        'update': se.PostCreateSerializer,
        'partial_update': se.PostCreateSerializer,
        'rate': se.RateSerializer,
        'add_media': se.MediaSerializer,
        'buy': se.PostCreateSerializer,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action)

    def retrieve(self, request, **kwargs):
        try:
            instance = Post.objects.filter(pk=kwargs['pk']).annotate(
                average_rate=Avg('rates__rate')
            ).prefetch_related(
                'viewed_by', 'medias__special_users', 'special_users', 'page__special_users'
            )[0]
        except ObjectDoesNotExist:
            return Response({'error': 'the post by id = {} does not exist'.format(kwargs['pk'])})

        if request.user.is_authenticated:
            user = Profile.objects.get(username=get_user_by_token(request))
            if user not in instance.viewed_by.all():
                instance.viewed_by.add(user)
            if instance.price != 0 or False in [media.price != 0 for media in instance.medias.all()]:
                if user in instance.special_users.all() or user in instance.page.special_users.all():
                    post = se.PostDetailSerializer(instance, context={'request': request})
                    files = se.MediaSerializer(instance.medias, many=True, context={'request': request})
                    return Response({
                        'post info': post.data,
                        'files': files.data,
                        'hide_files': [],
                        'rate': instance.average_rate
                    })
                else:
                    post = se.PostDetailSerializer(instance, context={'request': request})
                    files = []
                    hide_files = []
                    medias = instance.medias.all()
                    for media in medias:
                        if not media.is_special or user in media.special_users.all():
                            files.append(se.MediaSerializer(media, context={'request': request}).data)
                        else:
                            hide_files.append(se.HideMediaSerializer(media, context={'request': request}).data)
                    return Response({
                        'post info': post.data,
                        'files': files,
                        'hide_files': hide_files,
                        'rate': instance.average_rate
                    })
            else:
                post = se.PostDetailSerializer(instance, context={'request': request})
                files = se.MediaSerializer(instance.medias, many=True, context={'request': request})
                return Response({
                    'post info': post.data,
                    'files': files.data,
                    'hide_files': [],
                    'rate': instance.average_rate
                })
        else:
            post = se.PostDetailSerializer(instance, context={'request': request})
            files = []
            hide_files = []
            medias = instance.medias.all()
            for media in medias:
                if not media.is_special:
                    files.append(se.MediaSerializer(media, context={'request': request}).data)
                else:
                    hide_files.append(se.HideMediaSerializer(media, context={'request': request}).data)
            return Response({
                'post info': post.data,
                'files': files,
                'hide_files': hide_files,
                'rate': instance.average_rate
            })

    @action(methods=['post'], detail=True)
    def rate(self, request, **kwargs):
        if request.user.is_authenticated:
            rate(request.user, kwargs['pk'], request.data['rate'])
            return HttpResponseRedirect(reverse('post-detail', kwargs={'pk': kwargs['pk']}))
        else:
            return HttpResponseRedirect(reverse('login'))

    @action(methods=['get'], detail=True)
    def buy(self, request, **kwargs):
        if request.user.is_authenticated:
            buy(request.user, kwargs['pk'])
            return HttpResponseRedirect(reverse('post-detail', kwargs={'pk': kwargs['pk']}))
        else:
            return HttpResponseRedirect(reverse('login'))

    @action(methods=['put'], detail=True)
    def add_media(self, request, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            post = Post.objects.get(pk=kwargs['pk'])
            MediaFile.objects.create(file=data['file'], post=post, price=data['price'])
            return Response({'status': 'media added'})
        else:
            return HttpResponseRedirect(reverse('post-detail', kwargs={'pk': kwargs['pk']}))


def media_buy(request, post_id, media_id):
    if request.user.is_authenticated:
        buy_media(request.user, media_id)
        return HttpResponseRedirect(reverse('post-detail', kwargs={'pk': post_id}))
    else:
        return HttpResponseRedirect(reverse('login'))
