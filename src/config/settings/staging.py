from . import *

'''
staging settings
settings intended for use inside a staging version of your application
'''

# are we in debug mode?
# no django debug in staging
# please refer to logs defined in /srv/logs/
# this is set up in docker-entrypoint.sh
DEBUG = False

# specify the db for staging
# this should be the name corresponding to a key in defaults.database DATABASES
DB_MAIN = 'yourcompany_mvp_staging'