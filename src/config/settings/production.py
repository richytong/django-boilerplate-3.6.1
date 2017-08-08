from . import *

'''
production settings
settings intended for use inside the production version of your application
'''

# are we in debug mode?
# no django debug in production
# please refer to logs defined in /srv/logs/
# this is set up in docker-entrypoint.sh
DEBUG = False

# specify the db for production
# this should be the name corresponding to a key in defaults.database DATABASES
DB_MAIN = 'yourcompany_mvp_production'

# use secure cookies
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True