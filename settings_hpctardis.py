# Note that this is a deployment script with hardcoded paths

from os import path
from tardis.settings_changeme import *

# Debug mode
DEBUG = False

# Database settings
DATABASES = {
    'default': {
        # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.sqlite3',
        # Name of the database to use. For SQLite, it's the full path.
        'NAME': '/home/user/CoreTardis/tardis.sql',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Root URLs in HPCTardi
ROOT_URLCONF = 'tardis.apps.hpctardis.urls'

# extend template directory to TEMPLATE_DIRS
tmp = list(TEMPLATE_DIRS)
tmp.append(path.join(path.dirname(__file__),
                     'apps/hpctardis/publish/').replace('\\', '/'),
    )
tmp.append(path.join(path.dirname(__file__),
                     'tardis_portal/publish/').replace('\\', '/'),
    )
TEMPLATE_DIRS = tuple(tmp)

# Post Save Filters
tmp = list(POST_SAVE_FILTERS)
tmp.append(("tardis.apps.microtardis.filters.exiftags.make_filter", ["MICROSCOPY_EXIF","http://rmmf.isis.rmit.edu.au/schemas"]))
tmp.append(("tardis.apps.microtardis.filters.spctags.make_filter", ["EDAXGenesis_SPC","http://rmmf.isis.rmit.edu.au/schemas"]))
tmp.append(("tardis.apps.hpctardis.filters.metadata.make_filter", ["",""]))
POST_SAVE_FILTERS = tuple(tmp)


ADMIN_MEDIA_STATIC_DOC_ROOT = path.join(path.dirname(__file__),'../eggs/Django-1.3-py2.6.egg/django/contrib/admin/media/').replace('\\', '/')

STAGING_PATH = path.abspath('/home/user/dcweb.staging/').replace('\\', '/')
STAGING_PROTOCOL = 'localdb'

# Directory path for image thumbnails
THUMBNAILS_PATH = path.abspath(path.join(path.dirname(__file__),
    '../var/thumbnails/')).replace('\\', '/')

INSTALLED_APPS = (TARDIS_APP_ROOT+".hpctardis",
                  'django.contrib.markup',
                  'django_nose',) + INSTALLED_APPS

# Template loaders
TEMPLATE_LOADERS = (
    'tardis.apps.microtardis.templates.loaders.app_specific.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.filesystem.Loader',
)


# HPCTardis Media
HPC_STATIC_URL_ROOT = '/static'
HPC_STATIC_DOC_ROOT = path.join(path.dirname(__file__),
                               'apps/hpctardis/static').replace('\\', '/')
                               

# logging levels are: DEBUG, INFO, WARN, ERROR, CRITICAL
SYSTEM_LOG_LEVEL = 'INFO'
MODULE_LOG_LEVEL = 'INFO'

SYSTEM_LOG_FILENAME = '/var/www/tardis/request.log'
MODULE_LOG_FILENAME = '/var/www/tardis/tardis.log'

EMAIL_PORT = 587 
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'eresearch.rmit@gmail.com'     
EMAIL_HOST_PASSWORD = 'PASSWORD'
EMAIL_USE_TLS = True
EMAIL_LINK_HOST = "http://gaia1.isis.rmit.edu.au:8890"

# The anzsrc codes for subject for all collections
COLLECTION_SUBJECTS = ['0307','0204']
GROUP = "RMIT University"
GROUP_ADDRESS = "Applied Science, RMIT University, Melbourne VIC 3000, Australia"
ACCESS_RIGHTS= "Contact the researchers/parties associated with this dataset"
RIGHTS= "Terms and conditions applies as specified by the researchers"

# Priviate datafiles
PRIVATE_DATAFILES = True

# LDAP configuration
LDAP_USE_TLS = False
LDAP_URL = "ldap://localhost:38911/"
LDAP_USER_LOGIN_ATTR = "uid"
LDAP_USER_ATTR_MAP = {"givenName": "display", "mail": "email"}
LDAP_GROUP_ID_ATTR = "cn"
LDAP_GROUP_ATTR_MAP = {"description": "display"}
#LDAP_ADMIN_USER = ''
#LDAP_ADMIN_PASSWORD = ''
LDAP_BASE = 'dc=example, dc=com'
LDAP_USER_BASE = 'ou=People, ' + LDAP_BASE
LDAP_GROUP_BASE = 'ou=Group, ' + LDAP_BASE

# Publish Providers Configuration
PUBLISH_PROVIDERS = (
                    'tardis.apps.hpctardis.publish.rif_cs_profile.'
                    + 'rif_cs_PublishProvider.rif_cs_PublishProvider',
                    )
# Test Runner Configuration
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Staging Protocol
STAGING_PROTOCOL = 'localdb'
GET_FULL_STAGING_PATH_TEST = path.join(STAGING_PATH, "test_user")

# AUTH_PROVIDERS 
AUTH_PROVIDERS = (
    ('localdb', 'Local DB', 'tardis.tardis_portal.auth.localdb_auth.DjangoAuthBackend'),
    ('ldap', 'LDAP', 'tardis.tardis_portal.auth.ldap_auth.ldap_auth'),
)

# Email
EMAIL_LINK_HOST = "http://127.0.0.1:8080"

# Default institution
DEFAULT_INSTITUTION = "RMIT University"
