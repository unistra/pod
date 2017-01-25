[uwsgi]
virtualenv = {{ remote_virtualenv_dir }}
chdir = {{ remote_current_path }}
module={{ root_package_name }}.wsgi:application
processes = 2
master=True
vacuum=True
max-requests=5000
daemonize={{ remote_shared_path }}/log/%n.log
env = DJANGO_SETTINGS_MODULE={{ root_package_name }}.settings.{{ goal }}
uid = {{ remote_owner }}
gid = {{ remote_group }}
http-socket={% if socket_host %}{{ socket_host }}{% else %}{{ host }}{% endif %}:{{ socket_port }}
limit-post=0
socket-timeout=1800
chunked-input-timeout=1800
http-timeout=1800
