from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import Http404
from django.utils.functional import cached_property

from rest_framework import serializers

from cms.common import mixins
from .models import (
    Category, Article, ArticleImage, ContentModule, ArticlesModule,
    CategoriesModule
)


class ArticleImageSerializer(serializers.ModelSerializer):
    full_size = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = ArticleImage
        fields = ('full_size', 'thumbnail', 'title')

    def get_thumbnail(self, obj):
        return obj.get_thumbnail(request=self.context['request'])

    def get_full_size(self, obj):
        return obj.get_full_size(request=self.context['request'])

    def to_representation(self, obj):
        data = super(ArticleImageSerializer, self).to_representation(obj)
        if not data.get('title'):
            data.pop('title')
        return data


class ArticleSerializer(serializers.ModelSerializer):
    images = ArticleImageSerializer(many=True)

    class Meta:
        model = Article
        fields = ('pk', 'title', 'category', 'intro', 'content', 'images',
                  'created', 'breadcrumbs', 'back_link')

    def to_representation(self, obj):
        data = super(ArticleSerializer, self).to_representation(obj)
        if not obj.show_created:
            data.pop('created')
        if not obj.show_breadcrumbs:
            data.pop('breadcrumbs')
        if not obj.show_back_link:
            data.pop('back_link')
        return data


class SubcategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('pk', 'name', 'route', 'description', 'image')

    def get_image(self, obj):
        return obj.parent.get_subcategory_image(
            category=obj, request=self.context['request']
        )

    def to_representation(self, obj):
        data = super(SubcategorySerializer, self).to_representation(obj)
        if not obj.parent.show_subcategories_descriptions:
            data.pop('description')
        if not obj.parent.show_subcategories_images or not data.get('image'):
            data.pop('image')
        return data


class CategoryArticleSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('pk', 'title', 'route', 'intro', 'content', 'image',
                  'created')

    def get_image(self, obj):
        return obj.category.get_article_image(
            article=obj, request=self.context['request']
        )

    def to_representation(self, obj):
        data = super(CategoryArticleSerializer, self).to_representation(obj)
        if not obj.category.show_articles_intros:
            data.pop('intro')
        if not obj.category.show_articles_contents:
            data.pop('content')
        if not obj.category.show_articles_images or not data.get('image'):
            data.pop('image')
        if not obj.category.show_articles_created:
            data.pop('created')
        return data


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True)
    image = serializers.SerializerMethodField()
    articles = serializers.SerializerMethodField()
    pagination = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('pk', 'name', 'description', 'image', 'subcategories',
                  'articles', 'pagination', 'breadcrumbs', 'back_link')

    @cached_property
    def _pagination(self):
        if self.instance.pagination:
            query_page = self.context['request'].GET.get('page') or 1
            try:
                paginator = Paginator(
                    self.instance.articles,
                    self.instance.articles_on_page
                )
                return paginator.page(query_page)
            except InvalidPage:
                raise Http404
        else:
            return None

    def get_image(self, obj):
        return obj.get_image(request=self.context['request'])

    def get_articles(self, obj):
        if self._pagination:
            articles = self._pagination.object_list
        else:
            articles = obj.articles
        return CategoryArticleSerializer(
            articles, many=True, context={'request': self.context['request']}
        ).data

    def get_pagination(self, obj):
        if self._pagination and self._pagination.paginator.num_pages > 1:
            return {
                'count': self._pagination.paginator.count,
                'num_pages': self._pagination.paginator.num_pages,
                'current_page': self._pagination.number
            }
        else:
            return None

    def to_representation(self, obj):
        data = super(CategorySerializer, self).to_representation(obj)
        if not obj.pagination:
            data.pop('pagination')
        if not obj.show_description:
            data.pop('description')
        if not obj.show_image:
            data.pop('image')
        if not obj.show_breadcrumbs:
            data.pop('breadcrumbs')
        if not obj.show_back_link:
            data.pop('back_link')
        return data


class ContentModuleSerializer(mixins.ModuleSerializer):
    class Meta:
        model = ContentModule
        fields = ('pk', 'name', 'module_name_header_level', 'html_class',
                  'content')


class ArticlesModuleItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('pk', 'title', 'intro', 'content', 'image', 'route')

    def get_image(self, obj):
        module = self.root.instance
        return module.get_article_image(
            article=obj, request=self.context['request']
        )

    def to_representation(self, obj):
        data = super(ArticlesModuleItemSerializer, self).to_representation(obj)
        module = self.root.instance
        if not module.show_articles_titles or not data.get('title'):
            data.pop('title')
        if not module.show_articles_intros or not data.get('intro'):
            data.pop('intro')
        if not module.show_articles_contents or not data.get('content'):
            data.pop('content')
        if not module.show_articles_images or not data.get('image'):
            data.pop('image')
        if not obj.route:
            data.pop('route')
        return data


class ArticlesModuleSerializer(mixins.ModuleSerializer):
    articles = ArticlesModuleItemSerializer(many=True, source='items')

    class Meta:
        model = ArticlesModule
        fields = ('pk', 'name', 'module_name_header_level', 'html_class',
                  'articles', 'articles_titles_headers_level')

    def to_representation(self, obj):
        data = super(ArticlesModuleSerializer, self).to_representation(obj)
        if not obj.show_articles_titles:
            data.pop('articles_titles_headers_level')
        return data


class CategoriesModuleItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('pk', 'name', 'description', 'image', 'route')

    def get_image(self, obj):
        module = self.root.instance
        return module.get_category_image(
            category=obj, request=self.context['request']
        )

    def to_representation(self, obj):
        data = super(CategoriesModuleItemSerializer, self) \
            .to_representation(obj)
        module = self.root.instance
        if not module.show_names or not data.get('name'):
            data.pop('name')
        if (
            not module.show_descriptions or
            not data.get('description')
        ):
            data.pop('description')
        if not module.show_images or not data.get('image'):
            data.pop('image')
        if not obj.route:
            data.pop('route')
        return data


class CategoriesModuleSerializer(mixins.ModuleSerializer):
    categories = CategoriesModuleItemSerializer(many=True, source='items')

    class Meta:
        model = CategoriesModule
        fields = ('pk', 'name', 'module_name_header_level', 'html_class',
                  'categories', 'names_headers_level')

    def to_representation(self, obj):
        data = super(CategoriesModuleSerializer, self).to_representation(obj)
        if not obj.show_names:
            data.pop('names_headers_level')
        return data
