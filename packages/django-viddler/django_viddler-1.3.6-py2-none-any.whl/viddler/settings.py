# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from pyviddler import ViddlerAPI

DEFAULT_SETTINGS = {
    'API_KEY': None,
    'USERNAME': None,
    'PASSWORD': None,
    'KEY_IMAGE_STORAGE': settings.DEFAULT_FILE_STORAGE,
    'THUMB_SIZE': (200, 200),
    'EDITABLE_VIDDLER_FIELDS': (  # These fields can trigger a sync when changed
        'title', 'description', 'tags', 'permalink', 'age_limit', 'tags',
        'view_permission', 'embed_permission', 'tagging_permission',
        'commenting_permission', 'download_permission',
    ),
    'NONOVERWRITABLE_VIDDLER_FIELDS': (  # These fields can't be changed from Viddler
    ),
}

USER_SETTINGS = DEFAULT_SETTINGS.copy()
USER_SETTINGS.update(getattr(settings, 'VIDDLER_SETTINGS', {}))

if (USER_SETTINGS['API_KEY'] is None or USER_SETTINGS['USERNAME'] is None or
        USER_SETTINGS['PASSWORD'] is None):
    raise ImproperlyConfigured("Please set the API_KEY, USERNAME and PASSWORD of VIDDLER_SETTINGS")

PERMISSIONS = (
    ('private', 'Private (Only Me)'),
    ('invite', 'Invitation Only (Anyone with an invitation)'),
    ('embed', 'Domain Restricted (Anyone on allowed domains)'),
    ('public', 'Public (Everyone)'),
)


def get_viddler():
    return ViddlerAPI(
        USER_SETTINGS['API_KEY'],
        USER_SETTINGS['USERNAME'],
        USER_SETTINGS['PASSWORD'],
    )

globals().update(USER_SETTINGS)
