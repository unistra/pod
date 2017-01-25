# -*- coding: utf-8 -*-

"""
uwsgi
=====

Required functions for uwsgi

"""

from os.path import dirname, join, sep

import fabric
import fabtools
from fabric.api import env
from pydiploy.decorators import do_verbose


@do_verbose
def install_uwsgi(update=False):
    """ install uwsgi """

    # install package with pip on the system
    fabtools.require.python.install(env.get('uwsgi_package_name', 'uwsgi'),
                                    use_sudo=True, upgrade=update)

    # init file for uwsgi with the emperor mode
    fabtools.files.upload_template(
        'emperor.uwsgi.service.tpl',
        join(sep, 'etc', 'systemd', 'system', 'emperor.uwsgi.service'),
        context=env,
        template_dir=join(
            dirname(__file__), 'templates'),
        use_sudo=True,
        user='root',
        chown=True,
        mode='644',
        use_jinja=True)

    # Directories for apps
    uwsgi_root = '/etc/uwsgi'
    uwsgi_available = join(uwsgi_root, 'apps-available')
    uwsgi_enabled = join(uwsgi_root, 'apps-enabled')
    fabtools.require.files.directories([
        uwsgi_root, uwsgi_available, uwsgi_enabled], use_sudo=True,
        owner=env.remote_owner, group=env.remote_group, mode='750')

    # reload systemd conf
    fabric.api.run('systemctl daemon-reload')
    fabtools.systemd.restart("emperor.uwsgi")


@do_verbose
def app_uwsgi_conf():
    """ app uwsgi conf """
    # app config
    uwsgi_root = '/etc/uwsgi'
    uwsgi_available = join(uwsgi_root, 'apps-available')
    uwsgi_enabled = join(uwsgi_root, 'apps-enabled')
    app_conf = join(uwsgi_available, '%s.ini' % env.server_name)
    fabtools.files.upload_template('uwsgi-app.ini.tpl',
                                   app_conf,
                                   context=env,
                                   template_dir=join(
                                       dirname(__file__), 'templates'),
                                   use_jinja=True,
                                   use_sudo=True,
                                   user=env.remote_owner,
                                   chown=True,
                                   mode='644')

    if not fabtools.files.is_link('%s/%s.ini' % (uwsgi_enabled,
                                                  env.server_name)):
        with fabric.api.cd(uwsgi_enabled):
            fabric.api.sudo('ln -s %s .' % app_conf)


@do_verbose
def uwsgi_restart():
    """ Starts/Restarts uwsgi """
    fabtools.systemd.restart("emperor.uwsgi")
