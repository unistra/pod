# -*- coding: utf-8 -*-

"""
celery
=====

Required functions for Celery

"""

from os.path import dirname, join, sep

import fabric
import fabtools
from fabric.api import env
from pydiploy.decorators import do_verbose


@do_verbose
def install_celery():
    if all([e in env.keys() for e in ('celery_version',)]):
        celery_filename = 'celery-%s' % env.application_name

        # create log folder
        fabtools.require.files.directory(
            path=join(sep, "var", "log", "celery"),
            use_sudo=True,
            owner=env.remote_owner,
            group=env.remote_group,
            mode='775')

        # create run folder
        fabtools.require.files.directory(
            path=join(sep, "var", "run", "celery"),
            use_sudo=True,
            owner=env.remote_owner,
            group=env.remote_group,
            mode='775')

        # Daemon file in /etc/systemd/system
        systemd_path = join(sep, 'etc', 'systemd', 'system')
        celerysystem_filepath = join(systemd_path, celery_filename + ".service")
        with fabric.api.cd(systemd_path):
            fabtools.files.upload_template('celery.service.tpl',
                                           celerysystem_filepath,
                                           context=env,
                                           template_dir=join(
                                               dirname(__file__), 'templates'),
                                           use_jinja=True,
                                           use_sudo=True,
                                           user='root',
                                           chown=True,
                                           mode='755')

        # Configuration file in /etc/default
        celeryd_path = join(sep, 'etc', 'default')
        celeryd_filepath = join(celeryd_path, celery_filename)

        with fabric.api.cd(celeryd_path):
            fabtools.files.upload_template('celery.tpl',
                                           celeryd_filepath,
                                           context=env,
                                           template_dir=join(
                                               dirname(__file__), 'templates'),
                                           use_jinja=True,
                                           use_sudo=True,
                                           user='root',
                                           chown=True,
                                           mode='644')

        # start celery
        fabric.api.run('systemctl daemon-reload')
        fabtools.systemd.restart(celery_filename)


    else:
        fabric.api.abort('Please provide parameters for Celery installation !')


@do_verbose
def deploy_celery_file():
    """ Uploads wsgi.py template on remote """
    fabtools.files.upload_template('celery.py',
                                   join(
                                       env.remote_base_package_dir,
                                       'celery.py'
                                   ),
                                   template_dir=env.local_tmp_root_app_package,
                                   context=env,
                                   use_sudo=True,
                                   user=env.remote_owner,
                                   chown=True,
                                   mode='644',
                                   use_jinja=True)
