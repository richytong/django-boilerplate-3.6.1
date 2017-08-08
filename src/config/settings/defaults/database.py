'''
Place database credentials for your project here
This boilerplate intends to use PostGreSQL and provides and example django psql configuration
'''
import os

# Specify the project root now that settings is not in its default place
# you will not need these relative paths if you use a postgres server on rds
CURRENT_FILE = os.path.abspath(__file__)
PROJECT_ROOT = os.path.join(os.path.dirname(CURRENT_FILE), '../../..')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'db.sqlite3'),
    },
#    'yourcompany_mvp': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': 'yourcompany_mvp',                      
#        'USER': 'youruser',
#        'PASSWORD': 'yourpassword',
#        'HOST': 'yourrdshost.providedbyaws.us-east-1.rds.amazonaws.com',
#        'PORT': '5432',
#    }
}