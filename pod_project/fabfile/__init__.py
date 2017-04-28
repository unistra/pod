# -*- coding: utf-8 -*-

"""
"""

from fabric.api import (env, roles, execute, task, sudo, warn_only)
from os.path import join
import fabtools
import pydiploy
from fabric.operations import put
from .celery import install_celery, deploy_celery_file, celery_restart
from .uwsgi import install_uwsgi, uwsgi_restart, app_uwsgi_conf


# edit config here !

env.remote_owner = 'django'  # remote server user
env.remote_group = 'di'  # remote server group

env.application_name = 'pod'   # name of webapp
env.root_package_name = 'pod_project'  # name of app in webapp

env.remote_home = '/home/django'  # remote home root
env.remote_python_version = '2.7'  # python version
env.remote_virtualenv_root = join(env.remote_home, '.virtualenvs')  # venv root
env.remote_virtualenv_dir = join(env.remote_virtualenv_root,
                                 env.application_name)  # venv for webapp dir
# git repository url
env.remote_repo_url = '../.' # Relative git local folder because github doesn't support git archive
env.remote_repo_specific_folder = 'pod_project' # specify a subfolder for the remote repository
env.local_tmp_dir = '/tmp'  # tmp dir
env.remote_static_root = '/var/www/static/'  # root of static files
env.locale = 'fr_FR.UTF-8'  # locale to use on remote
env.timezone = 'Europe/Paris'  # timezone for remote
env.keep_releases = 2  # number of old releases to keep before cleaning
env.extra_goals = ['preprod', 'utvtest']  # add extra goal(s) to defaults (test,dev,prod)
env.dipstrap_version = 'latest'
env.verbose_output = True # True for verbose output

# celery parameters
env.celery_version = '3.1'

# optional parameters

# env.dest_path = '' # if not set using env_local_tmp_dir
# env.excluded_files = ['pron.jpg'] # file(s) that rsync should exclude when deploying app
# env.extra_ppa_to_install = ['ppa:vincent-c/ponysay'] # extra ppa source(s) to use
env.extra_pkg_to_install = ['gcc', 'g++', 'libmysqlclient-dev','graphviz','libgraphviz-dev', 'pkg-config', 'libldap2-dev', 'libsasl2-dev',
        'libssl-dev', 'libjpeg-dev', 'python-imaging', 'libfreetype6-dev', 'python-chardet', 'python-fpconst', 'python-apt', 'python-debian',
        'python-debianbts', 'python-reportbug', ' python-soappy','memcached', 'gettext', 'libldap2-dev', 'libsasl2-dev', 'libssl-dev', 'libpq-dev'] # extra debian/ubuntu package(s) to install on remote
# env.cfg_shared_files = ['config','/app/path/to/config/config_file'] # config files to be placed in shared config dir
# env.extra_symlink_dirs = ['mydir','/app/mydir'] # dirs to be symlinked in shared directory
env.verbose = True # verbose display for pydiploy default value = True
# env.req_pydiploy_version = "0.9" # required pydiploy version for this fabfile
# env.no_config_test = False # avoid config checker if True
# env.maintenance_text = "" # add a customize maintenance text for maintenance page
# env.maintenance_title = "" # add a customize title for maintenance page
# env.oracle_client_version = '11.2'
# env.oracle_download_url = 'http://librepo.net/lib/oracle/'
# env.oracle_remote_dir = 'oracle_client'
# env.oracle_packages = ['instantclient-basic-linux-x86-64-11.2.0.2.0.zip',
#                        'instantclient-sdk-linux-x86-64-11.2.0.2.0.zip',
#                        'instantclient-sqlplus-linux-x86-64-11.2.0.2.0.zip']
#
# env.circus_package_name = 'https://github.com/morganbohn/circus/archive/master.zip'
# env.no_circus_web = True
# env.circus_backend = 'gevent' # name of circus backend to use

# env.chaussette_backend = 'gevent' # name of chaussette backend to use. You need to add this backend in the app requirement file.

env.media_folder = '/media' # path of media folder
env.remote_media_folder = '/srv/media/pod' # root of media files

# env.nginx_start_confirmation = True # if True when nginx is not started
# needs confirmation to start it.

@task
def dev():
    """Define test stage"""
    env.user = 'vagrant'
    env.roledefs = {
        'web': ['192.168.1.2'],
        'lb': ['192.168.1.2'],
        'encoding': []
    }
    env.backends = ['127.0.0.1']
    env.server_name = 'podcast-dev.u-strasbg.fr'
    env.short_server_name = 'podcast-dev'
    env.static_folder = '/static/'
    env.server_ip = ''
    env.no_shared_sessions = False
    env.server_ssl_on = False
    env.nginx_location_extra_directives = [
        'client_max_body_size 4G', 'client_body_temp_path /tmp', 'proxy_connect_timeout 1800',
        'proxy_send_timeout 1800', 'proxy_read_timeout 1800', 'send_timeout 1800'
    ]
    env.goal = 'dev'
    env.socket_port = '8000'
    env.socket_host = '127.0.0.1'
    env.map_settings = {}
    execute(build_env)

@task
def test():
    """Define test stage"""
    env.user = 'root'
    env.roledefs = {
        'web': ['podcast-test.di.unistra.fr'],
        'lb': ['podcast-test.di.unistra.fr'],
        'encoding': ['podcast-test.di.unistra.fr']
    }
    env.backends = ['127.0.0.1']
    env.server_name = 'podcast-test.u-strasbg.fr'
    env.short_server_name = 'podcast-test'
    env.static_folder = '/static/'
    env.server_ip = ''
    env.no_shared_sessions = False
    env.server_ssl_on = True
    env.nginx_location_extra_directives = [
        'client_max_body_size 4G', 'proxy_request_buffering off', 'proxy_connect_timeout 1800',
        'proxy_send_timeout 1800', 'proxy_read_timeout 1800', 'send_timeout 1800'
    ]
    env.extra_pkg_to_install += ["rabbitmq-server"]
    env.path_to_cert = '/etc/ssl/certs/wildcard.u-strasbg.fr.pem'
    env.path_to_cert_key = '/etc/ssl/private/wildcard.u-strasbg.fr.key'
    env.goal = 'test'
    env.socket_port = '8000'
    env.socket_host = '127.0.0.1'
    env.map_settings = {
        'secret_key': "SECRET_KEY",
        'default_db_host': "DATABASES['default']['HOST']",
        'default_db_user': "DATABASES['default']['USER']",
        'default_db_password': "DATABASES['default']['PASSWORD']",
        'default_db_name': "DATABASES['default']['NAME']",
        'cas_server_url': "CAS_SERVER_URL",
        'auth_ldap_server_uri': "AUTH_LDAP_SERVER_URI",
        'auth_ldap_bind_dn': "AUTH_LDAP_BIND_DN",
        'auth_ldap_bind_password': "AUTH_LDAP_BIND_PASSWORD",
        'auth_ldap_base_dn': "AUTH_LDAP_BASE_DN",
        'avcast_db_uri': "AVCAST_DB_URI",
        'celery_broker': "CELERY_BROKER"
    }
    execute(build_env)


@task
def utvtest():
    """Define utv test stage"""
    env.user = 'root'
    env.roledefs = {
        'web': ['pod-utv-test.di.unistra.fr'],
        'lb': ['pod-utv-test.di.unistra.fr'],
        'encoding': ['pod-utv-test.di.unistra.fr']
    }
    env.backends = ['127.0.0.1']
    env.server_name = 'pod-utv-test.di.unistra.fr'
    env.short_server_name = 'pod-utv-test'
    env.static_folder = '/static/'
    env.server_ip = ''
    env.no_shared_sessions = False
    env.server_ssl_on = True
    env.nginx_location_extra_directives = [
        'client_max_body_size 4G', 'proxy_request_buffering off', 'proxy_connect_timeout 1800',
        'proxy_send_timeout 1800', 'proxy_read_timeout 1800', 'send_timeout 1800'
    ]
    env.extra_pkg_to_install += ["rabbitmq-server"]
    env.path_to_cert = '/etc/ssl/certs/wildcard.u-strasbg.fr.pem'
    env.path_to_cert_key = '/etc/ssl/private/wildcard.u-strasbg.fr.key'
    env.goal = 'utvtest'
    env.socket_port = '8000'
    env.socket_host = '127.0.0.1'
    env.map_settings = {
        'secret_key': "SECRET_KEY",
        'default_db_host': "DATABASES['default']['HOST']",
        'default_db_user': "DATABASES['default']['USER']",
        'default_db_password': "DATABASES['default']['PASSWORD']",
        'default_db_name': "DATABASES['default']['NAME']",
        'cas_server_url': "CAS_SERVER_URL",
        'auth_ldap_server_uri': "AUTH_LDAP_SERVER_URI",
        'auth_ldap_bind_dn': "AUTH_LDAP_BIND_DN",
        'auth_ldap_bind_password': "AUTH_LDAP_BIND_PASSWORD",
        'auth_ldap_base_dn': "AUTH_LDAP_BASE_DN",
        'avcast_db_uri': "AVCAST_DB_URI",
        'celery_broker': "CELERY_BROKER"
    }
    execute(build_env)
        
@task
def preprod():
    """Define preprod stage"""
    env.user = 'root'
    env.roledefs = {
        'web': ['podcast-w1-pprd.di.unistra.fr', 'podcast-w2-pprd.di.unistra.fr'],
        'lb': ['podcast-w1-pprd.di.unistra.fr', 'podcast-w2-pprd.di.unistra.fr'],
        'encoding': ['podcast-enc1-pprd.di.unistra.fr ', 'podcast-enc2-pprd.di.unistra.fr']
    }
    env.backends = ['127.0.0.1']
    env.server_name = 'podcast-pprd.unistra.fr'
    env.remote_media_folder = '/nfs/media/pod' # root of media files
    env.short_server_name = 'podcast-pprd'
    env.static_folder = '/static/'
    env.server_ip = ''
    env.no_shared_sessions = False
    env.server_ssl_on = True
    env.nginx_location_extra_directives = [
        'client_max_body_size 4G', 'proxy_request_buffering off', 'proxy_connect_timeout 1800',
        'proxy_send_timeout 1800', 'proxy_read_timeout 1800', 'send_timeout 1800'
    ]
    env.path_to_cert = '/local/ssl/unistra.fr.pem'
    env.path_to_cert_key = '/local/ssl/unistra.fr.key'
    env.goal = 'preprod'
    env.socket_port = '8000'
    env.socket_host = '127.0.0.1'
    env.map_settings = {
        'secret_key': "SECRET_KEY",
        'default_db_host': "DATABASES['default']['HOST']",
        'default_db_user': "DATABASES['default']['USER']",
        'default_db_password': "DATABASES['default']['PASSWORD']",
        'default_db_name': "DATABASES['default']['NAME']",
        'cas_server_url': "CAS_SERVER_URL",
        'auth_ldap_server_uri': "AUTH_LDAP_SERVER_URI",
        'auth_ldap_bind_dn': "AUTH_LDAP_BIND_DN",
        'auth_ldap_bind_password': "AUTH_LDAP_BIND_PASSWORD",
        'auth_ldap_base_dn': "AUTH_LDAP_BASE_DN",
        'avcast_db_uri': "AVCAST_DB_URI",
        'celery_broker': "CELERY_BROKER"
    }
    execute(build_env)




# dont touch after that point if you don't know what you are doing !


@task
def tag(version_number):
    """ Set the version to deploy to `version_number`. """
    execute(pydiploy.prepare.tag, version=version_number)


@roles(['web', 'lb'])
def build_env():
    execute(pydiploy.prepare.build_env)


@task
def pre_install():
    """Pre install of backend & frontend"""
    execute(pre_install_backend)
    execute(pre_install_frontend)
    execute(pre_install_encoding)


@roles('encoding')
@task
def pre_install_encoding():
    """ Setup encoding server """
    execute(pydiploy.require.system.add_user, commands=None)
    execute(pydiploy.require.system.set_locale)
    execute(pydiploy.require.system.set_timezone)
    execute(pydiploy.require.system.update_pkg_index)
    fabtools.require.deb.packages(['ffmpeg', 'ffmpegthumbnailer', 'imagemagick'], update=False)
    execute(pydiploy.django.application_packages)
    execute(pydiploy.require.python.virtualenv.virtualenv)


@roles('web')
@task
def pre_install_backend(commands='/usr/bin/rsync', update_uwsgi=False):
    """ Installs requirements for uwsgi & virtualenv env """
    execute(pydiploy.require.system.add_user, commands=commands)
    execute(pydiploy.require.system.set_locale)
    execute(pydiploy.require.system.set_timezone)
    execute(pydiploy.require.system.update_pkg_index)
    execute(pydiploy.django.application_packages)
    # execute(pydiploy.require.circus.circus_pkg, update=upgrade_circus)
    execute(pydiploy.require.python.virtualenv.virtualenv)
    # execute(pydiploy.require.circus.upstart)
    execute(install_uwsgi, update=update_uwsgi)


@roles('lb')
@task
def pre_install_frontend():
    """Setup server for frontend"""
    execute(pydiploy.django.pre_install_frontend)


@task
def deploy(update_pkg=False):
    """Deploy code on server"""
    execute(deploy_backend, update_pkg)
    execute(deploy_frontend)
    execute(deploy_encoding, update_pkg)


@roles('web')
@task
def deploy_backend(update_pkg=False, **kwargs):
    """Deploy code on server"""
    with pydiploy.django.wrap_deploy():
        execute(pydiploy.require.releases_manager.setup)
        execute(pydiploy.require.releases_manager.deploy_code)
        execute(pydiploy.require.django.utils.deploy_manage_file)
        execute(pydiploy.require.django.utils.deploy_wsgi_file)
        execute(deploy_celery_file)
        execute(
            pydiploy.require.python.utils.application_dependencies,
            update_pkg)
        execute(pydiploy.require.django.utils.app_settings, **kwargs)
        execute(pydiploy.require.django.command.django_prepare)
        execute(pydiploy.require.system.permissions)
        # execute(pydiploy.require.circus.app_reload)
        execute(uwsgi_restart)
        execute(pydiploy.require.releases_manager.cleanup)


@roles('lb')
@task
def deploy_frontend():
    """Deploy static files on load balancer"""
    execute(pydiploy.django.deploy_frontend)


@roles('encoding')
@task
def deploy_encoding(update_pkg=False, **kwargs):
    """Deploy static files on load balancer"""
    with pydiploy.django.wrap_deploy():
        execute(pydiploy.require.releases_manager.setup)
        execute(pydiploy.require.releases_manager.deploy_code)
        execute(pydiploy.require.django.utils.deploy_manage_file)
        execute(pydiploy.require.django.utils.deploy_wsgi_file)
        execute(deploy_celery_file)
        execute(
            pydiploy.require.python.utils.application_dependencies,
            update_pkg)
        execute(pydiploy.require.django.utils.app_settings, **kwargs)
        execute(pydiploy.require.django.command.django_prepare)
        execute(pydiploy.require.system.permissions)
        execute(pydiploy.require.releases_manager.cleanup)
        with warn_only():
            execute(celery_restart)


@roles('web')
@task
def rollback():
    """ Rolls back django webapp """
    execute(pydiploy.require.releases_manager.rollback_code)
    # execute(pydiploy.require.circus.app_reload)
    execute(uwsgi_restart)


@task
def post_install():
    """post install for backend & frontend"""
    execute(post_install_backend)
    execute(post_install_frontend)
    execute(post_install_encoding)


@roles('web')
@task
def post_install_backend():
    """ Post-installation of webapp"""
    #execute(pydiploy.require.circus.app_circus_conf)
    execute(app_uwsgi_conf)
    # execute(pydiploy.require.circus.app_reload)
    execute(uwsgi_restart)


@roles('lb')
@task
def post_install_frontend():
    """Post installation of frontend"""
    #execute(pydiploy.django.post_install_frontend)
    execute(pydiploy.require.nginx.web_configuration)
    put('nginx_with_load_balancer.patch', '/tmp/')
    sudo("patch /etc/nginx/sites-available/%s.conf < /tmp/nginx_with_load_balancer.patch" % env.server_name)
    execute(pydiploy.require.nginx.nginx_restart)


@roles('encoding')
@task
def post_install_encoding():
    """Post installation of encoding"""
    # CELERY CONF
    execute(install_celery)


@roles('web')
@task
def install_postgres(user=None, dbname=None, password=None):
    """Install Postgres on remote"""
    execute(pydiploy.django.install_postgres_server,
            user=user, dbname=dbname, password=password)


@task
def reload():
    """Reload backend & frontend"""
    execute(reload_frontend)
    execute(reload_backend)


@roles('lb')
@task
def reload_frontend():
    execute(pydiploy.django.reload_frontend)


@roles('web')
@task
def reload_backend():
    """ Reloads backend """
    execute(uwsgi_restart)


@roles('lb')
@task
def set_down():
    """ Set app to maintenance mode """
    execute(pydiploy.django.set_app_down)


@roles('lb')
@task
def set_up():
    """ Set app to up mode """
    execute(pydiploy.django.set_app_up)


@roles('web')
@task
def custom_manage_cmd(cmd):
    """ Execute custom command in manage.py """
    execute(pydiploy.django.custom_manage_command, cmd)
