# -*- coding: utf-8 -*-

from .base import *
from os.path import join, normpath, dirname, abspath, basename

######################
# Path configuration #
######################

DJANGO_ROOT = dirname(dirname(abspath(__file__)))
SITE_ROOT = dirname(DJANGO_ROOT)
SITE_NAME = basename(DJANGO_ROOT)

#######################
# Debug configuration #
#######################

ADMINS = (
    ('morgan.bohn', 'morgan.bohn@unistra.fr'),
    ('cvedrine', 'cvedrine@unistra.fr'),
)

DEBUG = False
TEMPLATE_DEBUG = False

##############
# Secret key #
##############

SECRET_KEY = '{{ secret_key }}'

############################
# Allowed hosts & Security #
############################

ALLOWED_HOSTS = [
    '.u-strasbg.fr',
    '.unistra.fr',
    '.di.unistra.fr',
    '127.0.0.1',
    '130.79.200.183',
    '130.79.200.197',
    '130.79.200.204',
    '130.79.200.162',

]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'ssl')

##################
# Cache template #
##################

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

##########################
# Database configuration #
##########################

DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
DATABASES['default']['PORT'] = '5432'
DATABASES['default']['HOST'] = '{{ default_db_host }}'
DATABASES['default']['USER'] = '{{ default_db_user }}'
DATABASES['default']['PASSWORD'] = '{{ default_db_password }}'
DATABASES['default']['NAME'] = '{{ default_db_name }}'


#######################
# Email configuration #
#######################

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
SERVER_EMAIL = 'root@{{ server_name }}'
EMAIL_SUBJECT_PREFIX = '[{{ application_name }}]'

##################
# Authentication #
##################

USE_CAS = True
CAS_SERVER_URL = '{{ cas_server_url }}'

USE_LDAP_TO_POPULATE_USER = True
AUTH_LDAP_SERVER_URI = '{{ auth_ldap_server_uri }}'
AUTH_LDAP_BIND_DN = '{{ auth_ldap_bind_dn }}'
AUTH_LDAP_BIND_PASSWORD = '{{ auth_ldap_bind_password }}'
AUTH_LDAP_SCOPE = 'ONELEVEL'

AUTH_LDAP_BASE_DN = '{{ auth_ldap_base_dn }}'
AUTH_LDAP_USER_SEARCH = (AUTH_LDAP_BASE_DN, "(uid=%(uid)s)")
AUTH_LDAP_UID_TEST = ""

AUTH_USER_ATTR_MAP = {
    'first_name': 'givenName',
    'last_name': 'sn',
    'email': 'mail',
    'affiliation': 'eduPersonPrimaryAffiliation'
}
AFFILIATION_STAFF = ('employee', 'faculty', 'researcher')

############
# Template #
############

TITLE_SITE = 'Pod'
TITLE_ETB = 'Université de Strasbourg'
DEFAULT_IMG = 'images/default.png'
FILTER_USER_MENU = ('[a-d]', '[e-h]', '[i-l]', '[m-p]', '[q-t]', '[u-z]')
TEMPLATE_THEME = 'unistra-simple'

LOGO_SITE = 'images/logo_compact_unistra.png'
LOGO_COMPACT_SITE = 'images/logo_black_compact_unistra.png'
LOGO_ETB = 'images/unistra_top-01.png'
LOGO_PLAYER = 'images/logo_white_compact_unistra.png'
SERV_LOGO = 'images/semm_unistra.png'

HELP_MAIL = 'di-info-pod@unistra.fr'
WEBTV = ''

##
# Settings for all template engines to be used
#
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (
            os.path.join(BASE_DIR, 'core', 'theme',
                         TEMPLATE_THEME, 'templates'),
            os.path.join(BASE_DIR, 'core', 'templates'),
            os.path.join(BASE_DIR, 'core', 'templates', 'flatpages'),
        ),
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                # Local contexts
                'core.context_processors.pages_menu',
                'core.context_processors.context_settings',
                'pods.context_processors.items_menu_header',
            ),
            'debug': DEBUG,
        },
    },
]


##
# Additional static files locations (theme)
#
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'core', 'theme', TEMPLATE_THEME, 'assets'),
)

######################
# Flash Media Server #
######################

FMS_LIVE_URL = ''
FMS_ROOT_URL = ''

#########
# Video #
#########

FFMPEG = 'nice -n 19 ffmpeg'
FFPROBE = 'nice -n 19 ffprobe'
VIDEO_EXT_ACCEPT = (
    '.3gp',
    '.avi',
    '.divx',
    '.flv',
    '.m2p',
    '.m4v',
    '.mkv',
    '.mov',
    '.mp4',
    '.mpeg',
    '.mpg',
    '.mts',
    '.wmv',
    '.mp3',
    '.ogg',
    '.wav',
    '.wma',
    '.webm'
)

########
# Misc #
########

REPORT_VIDEO_MAIL_TO = ['di-info-pod@unistra.fr']
MAX_UPLOAD_FILE_SIZE = "4 Go"
FILE_UPLOAD_TEMP_DIR = '/nfs/tmp/django'

##########
# Logger #
##########


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)s %(asctime)s %(name)s:%(lineno)s %(message)s'
         }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '{{ remote_current_path }}/log/app.log',
            'maxBytes': 209715200,
            'backupCount': 3,
            'formatter': 'default'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'INFO'
        },
        'elasticsearch': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'pod_project': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True
        }
    }
}

##############################
# Static files configuration #
##############################

STATIC_ROOT = normpath(join(SITE_ROOT, 'assets'))
STATIC_URL = '/static/'

##############################
# Media files configuration #
##############################

MEDIA_ROOT = "/nfs/media/pod"
MEDIA_URL = '/media/'

########################
# Disable webm and wav #
########################

ENCODE_WEBM = False
ENCODE_WAV = False

# ENCODE_OVER_SSH_CMD = "ssh -i ~/.ssh/pod_distribution django@podcast-enc$(shuf -i 1-2 -n 1)-pprd.di.unistra.fr"
# ENCODE_VIDEO_CMD = ENCODE_OVER_SSH_CMD + " '" + "%(ffprobe)s -v quiet -show_format -show_streams -print_format json -i %(src)s" + "'"
# #ADD_THUMBNAILS_CMD = "%(ffmpeg)s -i \"%(src)s\" -vf fps=\"fps=1/%(thumbnail)s,scale=%(scale)s\" -an -vsync 0 -f image2 -y %(out)s_%(num)s.png"
# ADD_THUMBNAILS_CMD = ENCODE_OVER_SSH_CMD + " '" + "nice -n 19 ffmpegthumbnailer -i \"%(src)s\" -s 256x256 -f -t 10%% -o %(out)s_2.png && nice -n 19 ffmpegthumbnailer -i \"%(src)s\" -s 256x256 -f -t 50%% -o %(out)s_3.png && nice -n 19 ffmpegthumbnailer -i \"%(src)s\" -s 256x256 -f -t 75%% -o %(out)s_4.png" + "'"
# #ADD_OVERVIEW_CMD = ENCODE_OVER_SSH_CMD + " '" + "%(ffmpeg)s -i \"%(src)s\" -vf \"thumbnail=%(thumbnail)s,scale=%(scale)s,tile=100x1:nb_frames=100:padding=0:margin=0\" -an -vsync 0 -y %(out)s" + "'"
# ADD_OVERVIEW_CMD = ENCODE_OVER_SSH_CMD + " '" + "for i in $(seq 0 99); do nice -n 19 ffmpegthumbnailer -t $i%% -s %(scale)s -c jpeg -i \"%(src)s\" -o %(out)s_strip$i.jpg; nice -n 19 montage -geometry +0+0 %(out)s %(out)s_strip$i.jpg %(out)s; done; rm %(out)s_strip*.jpg" + "'"
# #ENCODE_MP4_CMD = "%(ffmpeg)s -i %(src)s -codec:v libx264 -profile:v high -pix_fmt yuv420p -preset faster -b:v %(bv)s -maxrate %(bv)s -bufsize %(bufsize)s -vf scale=%(scale)s -force_key_frames \"expr:gte(t,n_forced*1)\" -deinterlace -codec:a aac -strict -2 -ar %(ar)s -ac 2 -b:a %(ba)s -movflags faststart -y %(out)s"
# ENCODE_MP4_CMD = ENCODE_OVER_SSH_CMD + " '" + "%(ffmpeg)s -i %(src)s -codec:v libx264 -profile:v high -pix_fmt yuv420p -preset faster -qp 27 -vf scale=%(scale)s -codec:a aac -strict -2 -ar 48000 -ac 2 -vbr 5 -movflags faststart -y %(out)s" + "'"
# ENCODE_WEBM_CMD = ENCODE_OVER_SSH_CMD + " '" + "%(ffmpeg)s -i %(src)s -codec:v libvpx -quality realtime -cpu-used 3 -b:v %(bv)s -maxrate %(bv)s -bufsize %(bufsize)s -qmin 10 -qmax 42 -codec:a libvorbis -y %(out)s" + "'"
# ENCODE_MP3_CMD = ENCODE_OVER_SSH_CMD + " '" + "%(ffmpeg)s -i %(src)s -vn -ar %(ar)s -ab %(ab)s -f mp3 -y %(out)s" + "'"
# ENCODE_WAV_CMD = ENCODE_OVER_SSH_CMD + " '" + "%(ffmpeg)s -i %(src)s -ar %(ar)s -ab %(ab)s -f wav -y %(out)s" + "'"

ENCODE_VIDEO_CMD = "%(ffprobe)s -v quiet -show_format -show_streams -print_format json -i %(src)s"
#ADD_THUMBNAILS_CMD = "%(ffmpeg)s -i \"%(src)s\" -vf fps=\"fps=1/%(thumbnail)s,scale=%(scale)s\" -an -vsync 0 -f image2 -y %(out)s_%(num)s.png"
ADD_THUMBNAILS_CMD = "nice -n 19 ffmpegthumbnailer -i \"%(src)s\" -s 256x256 -t 10%% -o %(out)s_2.png && nice -n 19 ffmpegthumbnailer -i \"%(src)s\" -s 256x256 -t 50%% -o %(out)s_3.png && nice -n 19 ffmpegthumbnailer -i \"%(src)s\" -s 256x256 -t 75%% -o %(out)s_4.png"
#ADD_OVERVIEW_CMD = "%(ffmpeg)s -i \"%(src)s\" -vf \"thumbnail=%(thumbnail)s,scale=%(scale)s,tile=100x1:nb_frames=100:padding=0:margin=0\" -an -vsync 0 -y %(out)s"
ADD_OVERVIEW_CMD = "rm %(out)s;for i in $(seq 0 99); do nice -n 19 ffmpegthumbnailer -t $i%% -s %(scale)s -c jpeg -i \"%(src)s\" -o %(out)s_strip$i.jpg; nice -n 19 montage -geometry +0+0 %(out)s %(out)s_strip$i.jpg %(out)s; done; rm %(out)s_strip*.jpg"
#ENCODE_MP4_CMD = "%(ffmpeg)s -i %(src)s -codec:v libx264 -profile:v high -pix_fmt yuv420p -preset faster -b:v %(bv)s -maxrate %(bv)s -bufsize %(bufsize)s -vf scale=%(scale)s -force_key_frames \"expr:gte(t,n_forced*1)\" -deinterlace -codec:a aac -strict -2 -ar %(ar)s -ac 2 -b:a %(ba)s -movflags faststart -y %(out)s"
ENCODE_MP4_CMD = "%(ffmpeg)s -i %(src)s -codec:v libx264 -profile:v high -pix_fmt yuv420p -preset faster -qp 27 -vf scale=%(scale)s -codec:a aac -strict -2 -ar 48000 -ac 2 -vbr 5 -movflags faststart -y %(out)s"
ENCODE_WEBM_CMD = "%(ffmpeg)s -i %(src)s -codec:v libvpx -quality realtime -cpu-used 3 -b:v %(bv)s -maxrate %(bv)s -bufsize %(bufsize)s -qmin 10 -qmax 42 -codec:a libvorbis -y %(out)s"
ENCODE_MP3_CMD = "%(ffmpeg)s -i %(src)s -vn -ar %(ar)s -ab %(ab)s -f mp3 -y %(out)s"
ENCODE_WAV_CMD = "%(ffmpeg)s -i %(src)s -ar %(ar)s -ab %(ab)s -f wav -y %(out)s"

####################
# Avcast migration #
####################

INSTALLED_APPS += ('migration_avcast',)
AVCAST_DB_URI = '{{ avcast_db_uri }}'
AVCAST_COURSE_DEFAULT_USERNAME = "di-info-pod@unistra.fr"
AVCAST_VOLUME_PATH = "/audiovideocours/cours/1"
AVCAST_COPY_MODES_LIST = ["FAKE", "LINK", "COPY"]
AVCAST_COPY_MODE = AVCAST_COPY_MODES_LIST[0]

#################
# Elasticsearch #
#################

#URL FOR ELASTICSEARCH ['host1', 'host2', ...]
ES_URL = ['192.168.250.3:9200/', '192.168.250.8:9200/']

#######################
# Custom cursus codes #
#######################

CURSUS_CODES = (
    ("0", "Autres"),
    ("C", "Conférence"),
    ("1", "Licence 1ère année"),
    ("2", "Licence 2ème année"),
    ("3", "Licence 3ème année"),
    ("4", "Master 1ère année"),
    ("5", "Master 2ème année"),
    ("6", "Doctorat")
)

# Media protection:
MEDIA_GUARD = True
MEDIA_GUARD_SALT = '{{ media_guard_salt }}'

# CELERY
CELERY_TO_ENCODE = True
CELERY_NAME = "pod_project"
CELERY_BACKEND = "amqp"
CELERY_BROKER = '{{ celery_broker }}'
