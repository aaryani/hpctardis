from os import path
from test_settings import *
from os import listdir, path
import logging
import djcelery

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

DEBUG = True

DATABASES = {
    'default': {
        # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.sqlite3',
        # Name of the database to use. For SQLite, it's the full path.
        'NAME': ':memory:',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Celery queue uses Django for persistence
BROKER_TRANSPORT = 'django'
# During testing it's always eager
CELERY_ALWAYS_EAGER = True

ROOT_URLCONF = 'tardis.urls'

FILE_STORE_PATH = path.abspath(path.join(path.dirname(__file__),
                                         '../var/store/'))
STAGING_PATH = path.abspath(path.join(path.dirname(__file__),
                                      "../var/staging/"))

STAGING_PROTOCOL = 'localdb'
STAGING_MOUNT_PREFIX = 'smb://localhost/staging/'

GET_FULL_STAGING_PATH_TEST = path.join(STAGING_PATH, "test_user")

SITE_ID = '1'

TEMPLATE_DIRS = ['.']

STATIC_DOC_ROOT = path.join(path.dirname(__file__),
                            'tardis_portal/site_media').replace('\\', '/')

MEDIA_ROOT = STATIC_DOC_ROOT

MEDIA_URL = '/site_media'
STATIC_URL = '/static/'

def get_admin_media_path():
    import pkgutil
    package = pkgutil.get_loader("django.contrib.admin")
    return path.join(package.filename, 'media')

ADMIN_MEDIA_STATIC_DOC_ROOT = get_admin_media_path()


AUTH_PROVIDERS = (('localdb', 'Local DB',
                  'tardis.tardis_portal.auth.localdb_auth.DjangoAuthBackend'),
                  ('vbl', 'VBL',
                   'tardis.tardis_portal.tests.mock_vbl_auth.MockBackend'),
                  ('ldap', 'LDAP',
                   'tardis.tardis_portal.auth.ldap_auth.ldap_auth'),
)
DEFAULT_AUTH = 'localdb'

USER_PROVIDERS = ('tardis.tardis_portal.auth.localdb_auth.DjangoUserProvider',)

GROUP_PROVIDERS = ('tardis.tardis_portal.auth.localdb_auth.DjangoGroupProvider',
                    'tardis.tardis_portal.auth.token_auth.TokenGroupProvider',
                   'tardis.tardis_portal.auth.ip_auth.IPGroupProvider'
)

DOWNLOAD_PROVIDERS = (
    ('vbl', 'tardis.tardis_portal.tests.mock_vbl_download'),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'tardis.tardis_portal.auth.AuthorizationMiddleware',
    'tardis.tardis_portal.logging_middleware.LoggingMiddleware',
    'django.middleware.transaction.TransactionMiddleware'
)

TARDIS_APP_ROOT = 'tardis.apps'

def get_all_tardis_apps():
    tardis_app_dir = TARDIS_APP_ROOT.replace('.', path.sep)
    names = filter(path.isdir, \
                   map(lambda name: tardis_app_dir+'/'+name,
                       listdir(tardis_app_dir)))
    return sorted(map(lambda name: name.replace(path.sep, '.') , names))

INSTALLED_APPS = get_all_tardis_apps() + [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.admin',
        'django.contrib.admindocs',
        'django_extensions',
        'tardis.tardis_portal',
        'tardis.tardis_portal.templatetags',
        'registration',
        'django_nose',
        'django_jasmine',
        'djcelery',
        'djkombu',
]

JASMINE_TEST_DIRECTORY = path.abspath(path.join(path.dirname(__file__),
                                                'tardis_portal',
                                                'tests',
                                                'jasmine'))

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

SYSTEM_LOG_LEVEL = logging.DEBUG
MODULE_LOG_LEVEL = logging.DEBUG

SYSTEM_LOG_FILENAME = 'request.log'
MODULE_LOG_FILENAME = 'tardis.log'

SYSTEM_LOG_MAXBYTES = 0
MODULE_LOG_MAXBYTES = 0

UPLOADIFY_PATH = '%s/%s' % (STATIC_URL, 'js/uploadify/')
UPLOADIFY_UPLOAD_PATH = '%s/%s' % (MEDIA_URL, 'uploads/')

DEFAULT_INSTITUTION = "Monash University"

IMMUTABLE_METS_DATASETS = True

# Settings for the single search box
# Set HAYSTACK_SOLR_URL to the location of the SOLR server instance
SINGLE_SEARCH_ENABLED = False
HAYSTACK_SITECONF = 'tardis.search_sites'
HAYSTACK_SEARCH_ENGINE = 'solr'
HAYSTACK_SOLR_URL = 'http://127.0.0.1:8080/solr'
if SINGLE_SEARCH_ENABLED:
    INSTALLED_APPS = INSTALLED_APPS + ('haystack',)
else:
    HAYSTACK_ENABLE_REGISTRATIONS = False

TOKEN_EXPIRY_DAYS = 30
TOKEN_LENGTH = 30
TOKEN_USERNAME = 'tokenuser'

# RIF-CS Settings
OAI_DOCS_PATH = 'tardis/tardis_portal/tests/rifcs/'
RIFCS_TEMPLATE_DIR = 'tardis/tardis_portal/tests/rifcs/'
RELATED_INFO_SCHEMA_NAMESPACE = 'http://www.tardis.edu.au/schemas/related_info/2011/11/10'

DOI_ENABLE = False
DOI_XML_PROVIDER = 'tardis.tardis_portal.ands_doi.DOIXMLProvider'
#DOI_TEMPLATE_DIR = path.join(TARDIS_DIR, 'tardis_portal/templates/tardis_portal/doi/')
DOI_TEMPLATE_DIR = path.join('tardis_portal/doi/')
DOI_APP_ID = ''
DOI_NAMESPACE = 'http://www.tardis.edu.au/schemas/doi/2011/12/07'
DOI_MINT_URL = 'https://services.ands.org.au/home/dois/doi_mint.php'
DOI_RELATED_INFO_ENABLE = False
DOI_BASE_URL='http://mytardis.example.com'

djcelery.setup_loader()

# ------------------------------------
# -- HPCTardis settings for testing --
# ------------------------------------


# Template directorises
TEMPLATE_DIRS = (
    
    path.join(path.dirname(__file__),
    'apps/hpctardis/publish/').replace('\\', '/'),

    path.join(path.dirname(__file__),
    'apps/hpctardis/templates/').replace('\\', '/'),

                 
    path.join(path.dirname(__file__),
    'tardis_portal/publish/').replace('\\', '/'),                 
    
    path.join(path.dirname(__file__),
    'tardis_portal/templates/').replace('\\', '/'),

    '.',
                  
)

DEFAULT_INSTITUTION = "RMIT University"

IMMUTABLE_METS_DATASETS = True

PUBLISH_PROVIDERS = (
                    'tardis.apps.hpctardis.publish.rif_cs_profile.'
                    + 'rif_cs_PublishProvider.rif_cs_PublishProvider',
                    )
 
# Post Save Filters
POST_SAVE_FILTERS = []
tmp = list(POST_SAVE_FILTERS)
tmp.append(("tardis.apps.hpctardis.filters.metadata.make_filter", ["",""]))
POST_SAVE_FILTERS = tuple(tmp)

# Add Middleware
tmp = list(MIDDLEWARE_CLASSES)
tmp.append(
    'tardis.tardis_portal.filters.FilterInitMiddleware'
)
MIDDLEWARE_CLASSES = tuple(tmp)

# The anzsrc codes for subject for all collections
COLLECTION_SUBJECTS = None
GROUP = "Acme University"
GROUP_ADDRESS = "Acme University, Coimbatore, India"
ACCESS_RIGHTS= "Contact the researchers/parties associated with this dataset"
RIGHTS= "Terms and conditions applies as specified by the researchers"

# HPCTardis Media
HPC_STATIC_URL_ROOT = '/static'
HPC_STATIC_DOC_ROOT = path.join(path.dirname(__file__),
                               'apps/hpctardis/static').replace('\\', '/')

# Changed because hpctardis overrides existing urls, which are called in testcases
#ROOT_URLCONF = 'tardis.apps.hpctardis.urls'

PRIVATE_DATAFILES = False
                     
MATPLOTLIB_HOME = path.abspath(path.join(path.dirname(__file__), 
                                         '../')).replace('\\', '/')

RIFCS_GROUP = "MyTARDIS Default Group"
RELATED_OTHER_INFO_SCHEMA_NAMESPACE = 'http://www.tardis.edu.au/schemas/experiment/annotation/2011/07/07'

EMAIL_LINK_HOST = "http://127.0.0.1:8080"
