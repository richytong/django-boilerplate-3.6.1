from .defaults.credentials import *
from .defaults.database import *
from .defaults.django import *
from .defaults.logging import *

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # include any further custom installed apps here
    # example: 'users' if you have an installed app named users
)