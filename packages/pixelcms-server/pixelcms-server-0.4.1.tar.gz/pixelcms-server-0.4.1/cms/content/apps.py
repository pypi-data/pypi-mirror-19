from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ContentConfig(AppConfig):
    name = 'cms.content'
    verbose_name = _('Content')
