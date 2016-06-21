# -*- coding: utf-8 -*-

from .base import *

#######################
# Debug configuration #
#######################

ADMINS = ()

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

FFMPEG = 'nice -19 /usr/local/ffmpeg/ffmpeg'
FFPROBE = 'nice -19 /usr/local/ffmpeg/ffprobe'

########
# Misc #
########

REPORT_VIDEO_MAIL_TO = ['']

######
# ES #
######

ES_URL = ['http://127.0.0.1:9211/']

