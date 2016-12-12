[Unit]
Description=Celery Service
After=network.target

[Service]
Type=forking
User=django
Group=di
EnvironmentFile=-/etc/default/celery-pod
WorkingDirectory={{ remote_current_path }}
ExecStart=/bin/sh -c '${CELERY_BIN} multi start $CELERYD_NODES -A $CELERY_APP --logfile=${CELERYD_LOG_FILE} --pidfile=${CELERYD_PID_FILE} $CELERYD_OPTS'
ExecStop=/bin/sh -c '${CELERY_BIN} multi stopwait $CELERYD_NODES --pidfile=${CELERYD_PID_FILE}'
ExecReload=/bin/sh -c '${CELERY_BIN} multi restart $CELERYD_NODES -A $CELERY_APP --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} --loglevel="${CELERYD_LOG_LEVEL}" $CELERYD_OPTS'

[Install]
WantedBy=multi-user.target
