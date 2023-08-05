from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SitecatsConfig(AppConfig):
    """Sitecats configuration."""

    name = 'sitecats'
    verbose_name = _('Site Categories')

    _cat_cache = None

    def get_categories_cache(self):
        return self._cat_cache

    def ready(self):
        """Instantiate global cache object when ready.

        :return:
        """
        from sitecats.utils import Cache
        self._cat_cache = Cache()
