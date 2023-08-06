from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from cms.common import mixins
from .models import (
    Category, Article, ArticleImage, ContentModule, ArticlesModule,
    ArticlesModuleArticle, ArticlesModuleCategory, CategoriesModule,
    CategoriesModuleCategory
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    def routes(self, obj):
        return '<br />'.join(
            '<a href="{0}">{0}</a>'.format(r) for r in obj.all_routes
        )
    routes.short_description = _('Routes')
    routes.allow_tags = True

    list_display = ('name', 'published', 'order', 'routes',  'parent',
                    'language')
    list_filter = ('published', 'parent', 'language')
    list_editable = ('published', 'order', 'language')
    search_fields = ('name',)
    readonly_fields = ('routes',)

    raw_id_fields = ('parent',)
    autocomplete_lookup_fields = {'fk': ['parent']}

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', ('published', 'order', 'language'),
                       'parent', 'description', 'image')
        }),
        (_('Category view settings - general'), {
            'fields': (
                'show_description', ('show_image', 'image_size'),
                ('show_breadcrumbs', 'show_back_link')
            )
        }),
        (_('Category view settings - subcategories'), {
            'fields': (
                'show_subcategories_descriptions',
                ('show_subcategories_images', 'subcategories_images_size')
            )
        }),
        (_('Category view settings - articles'), {
            'fields': (
                ('show_articles_intros', 'show_articles_contents'),
                'show_articles_created',
                ('show_articles_images', 'articles_images_size'),
                ('pagination', 'articles_on_page'),
            )
        }),
        (_('Article view settings'), {
            'fields': ('av_articles_images_size',)
        })
    ) + mixins.SeoAdmin.fieldsets

    class Media:
        js = mixins.TinyMCE.js


class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 0
    sortable_field_name = 'order'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    def routes(self, obj):
        return '<br />'.join(
            '<a href="{0}">{0}</a>'.format(r) for r in obj.all_routes
        )
    routes.short_description = _('Routes')
    routes.allow_tags = True

    def list_image(self, obj):
        image = obj.thumbnail_or_first_image
        if image:
            try:
                return '<img src="{}" alt="" />'.format(
                    image.version_generate('admin_thumbnail').url
                )
            except OSError:
                return None
        return None
    list_image.short_description = _('Image')
    list_image.allow_tags = True

    list_display = ('title', 'published', 'order', 'routes', 'list_image',
                    'category', 'language')
    list_filter = ('published', 'category', 'language')
    list_editable = ('published', 'order', 'language')
    search_fields = ('title',)
    readonly_fields = ('routes', 'list_image', 'last_modified',)

    raw_id_fields = ('category',)
    autocomplete_lookup_fields = {'fk': ['category']}

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', ('published', 'order', 'language'),
                       'category')
        }),
        (_('Content'), {
            'description': _('<strong>Intro</strong> is displayed in category '
                             'view and article view, <strong>Content</strong> '
                             'is displayed only in article view.'),
            'fields': ('intro', 'content')
        }),
        (None, {
            'classes': ('placeholder images-group',),
            'fields': ()
        }),
        (None, {
            'fields': ('thumbnail',)
        }),
        (_('View settings'), {
            'fields': ('show_created', ('show_breadcrumbs', 'show_back_link'),
                       'images_thumbnails_size')
        }),
        (_('Dates'), {
            'fields': (('created', 'last_modified'),)
        })
    ) + mixins.SeoAdmin.fieldsets

    inlines = (ArticleImageInline,)

    class Media:
        js = mixins.TinyMCE.js


@admin.register(ContentModule)
class ContentModuleAdmin(mixins.ModuleAdmin):
    fieldsets = mixins.ModuleAdmin.fieldsets + [
        (_('Content module'), {
            'fields': ('content',)
        })
    ]

    class Media:
        js = mixins.TinyMCE.js


class ArticlesModuleArticleInline(admin.TabularInline):
    model = ArticlesModuleArticle
    extra = 0
    sortable_field_name = 'order'

    raw_id_fields = ('article',)
    autocomplete_lookup_fields = {'fk': ['article']}


class ArticlesModuleCategoryInline(admin.TabularInline):
    model = ArticlesModuleCategory
    extra = 0
    sortable_field_name = 'order'

    raw_id_fields = ('category',)
    autocomplete_lookup_fields = {'fk': ['category']}


@admin.register(ArticlesModule)
class ArticlesModuleAdmin(mixins.ModuleAdmin):
    fieldsets = mixins.ModuleAdmin.fieldsets + [
        (None, {
            'classes': ('placeholder articlesmodulearticle_set-group',),
            'fields': ()
        }),
        (None, {
            'classes': ('placeholder articlesmodulecategory_set-group',),
            'fields': ()
        }),
        (_('Articles module'), {
            'fields': ('articles_limit',
                       ('show_articles_titles',
                        'articles_titles_headers_level'),
                       ('show_articles_images', 'articles_images_size'),
                       'show_articles_intros', 'show_articles_contents')
        })
    ]

    inlines = (ArticlesModuleArticleInline, ArticlesModuleCategoryInline)


class CategoriesModuleCategoryInline(admin.TabularInline):
    model = CategoriesModuleCategory
    extra = 0
    sortable_field_name = 'order'

    raw_id_fields = ('category',)
    autocomplete_lookup_fields = {'fk': ['category']}


@admin.register(CategoriesModule)
class CategoriesModuleAdmin(mixins.ModuleAdmin):
    fieldsets = mixins.ModuleAdmin.fieldsets + [
        (None, {
            'classes': ('placeholder categoriesmodulecategory_set-group',),
            'fields': ()
        }),
        (_('Categories module'), {
            'fields': (('show_names',
                        'names_headers_level'),
                       ('show_images', 'images_size'),
                       'show_descriptions')
        })
    ]

    inlines = (CategoriesModuleCategoryInline,)
