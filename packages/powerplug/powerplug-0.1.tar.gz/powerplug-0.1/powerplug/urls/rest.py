import logging

from django.conf.urls import include, url

from pkg_resources import working_set

from rest_framework import routers

logger = logging.getLogger(__name__)

router = routers.DefaultRouter(trailing_slash=False)
for entry in working_set.iter_entry_points('powerplug.rest'):
    try:
        router.register(entry.name, entry.load())
    except ImportError:
        logger.exception('Error importing %s', entry.name)

urlpatterns = url(r'^api/', include(router.urls, namespace='api')),
