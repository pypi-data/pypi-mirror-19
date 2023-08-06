import logging
from django.conf.urls import include, url
from pkg_resources import working_set

logger = logging.getLogger(__name__)
urlpatterns = []
for entry in working_set.iter_entry_points('powerplug.urls'):
    try:
        urlpatterns.append(
            url(r'^{0}/'.format(entry.name), include(entry.module_name, namespace=entry.name))
        )
    except ImportError:
        logger.exception('Error importing %s', entry.name)
