# -*- coding: utf-8 -*-

from .base import *

#######################
# Debug configuration #
#######################

ADMINS = ()

SECRET_KEY = 'S3CR3T'

##########################
# Database configuration #
##########################

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite',
    }
}

#######################
# Email configuration #
#######################

EMAIL_BACKEND = ''

##################
# Authentication #
##################

CAS_SERVER_URL = ''

USE_LDAP_TO_POPULATE_USER = False
AUTH_LDAP_SERVER_URI = ''
AUTH_LDAP_BIND_DN = ''
AUTH_LDAP_BIND_PASSWORD = ''

######################
# Flash Media Server #
######################

FMS_LIVE_URL = ''
FMS_ROOT_URL = ''

#########
# Video #
#########

FFMPEG = 'nice -n 19 /usr/local/ffmpeg/ffmpeg'
FFPROBE = 'nice -n 19 /usr/local/ffmpeg/ffprobe'

########
# Misc #
########

REPORT_VIDEO_MAIL_TO = ['']
MAX_UPLOAD_FILE_SIZE = "4 Go"
FILE_UPLOAD_TEMP_DIR = '/tmp'

######
# ES #
######

ES_URL = ['http://127.0.0.1:9211/']

ENCODE_VIDEO_CMD = "%(ffprobe)s -v quiet -show_format -show_streams -print_format json -i %(src)s"
ADD_THUMBNAILS_CMD = "%(ffmpeg)s -i \"%(src)s\" -vf fps=\"fps=1/%(thumbnail)s,scale=%(scale)s\" -an -vsync 0 -f image2 -y %(out)s_%(num)s.png"
ADD_OVERVIEW_CMD = "%(ffmpeg)s -i \"%(src)s\" -vf \"thumbnail=%(thumbnail)s,scale=%(scale)s,tile=100x1:nb_frames=100:padding=0:margin=0\" -an -vsync 0 -y %(out)s"
ENCODE_MP4_CMD = "%(ffmpeg)s -i %(src)s -codec:v libx264 -profile:v high -pix_fmt yuv420p -preset faster -b:v %(bv)s -maxrate %(bv)s -bufsize %(bufsize)s -vf scale=%(scale)s -force_key_frames \"expr:gte(t,n_forced*1)\" -deinterlace -codec:a aac -strict -2 -ar %(ar)s -ac 2 -b:a %(ba)s -movflags faststart -y %(out)s"
ENCODE_WEBM_CMD = "%(ffmpeg)s -i %(src)s -codec:v libvpx -quality realtime -cpu-used 3 -b:v %(bv)s -maxrate %(bv)s -bufsize %(bufsize)s -qmin 10 -qmax 42 -codec:a libvorbis -y %(out)s"
ENCODE_MP3_CMD = "%(ffmpeg)s -i %(src)s -vn -ar %(ar)s -ab %(ab)s -f mp3 -y %(out)s"
ENCODE_WAV_CMD = "%(ffmpeg)s -i %(src)s -ar %(ar)s -ab %(ab)s -f wav -y %(out)s"

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

# Protection des médias
MEDIA_GUARD = True
MEDIA_GUARD_SALT = "S3CR3T"

# CELERY
CELERY_NAME = "pod_project"
CELERY_BACKEND = "amqp"
CELERY_BROKER = "amqp://guest@localhost//"

##
# Video in draft mode can be shared
USE_PRIVATE_VIDEO = True