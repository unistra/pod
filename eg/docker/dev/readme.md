

# installation des dépendances

* Installer docker-engine : https://docs.docker.com/engine/installation/
* Installer docker compose : https://docs.docker.com/compose/install/

Exemple:

    # installer docker

    aptitude install docker-io

    # ajouter l'utilisateur courant au groupe docker
    # pour lui permettre de gérer les instances

    adduser $USER docker

    # installer docker-compose
    # * cf https://github.com/docker/compose/releases/latest pour un lien frais
    #   et une doc a jour
    # * dans l'exemple, `~/bin` est dans votre `$path`

    dl18=https://github.com/docker/compose/releases/download/1.8.0/
    bin=docker-compose-Linux-x86_64
    wget -O ~/bin/docker-compose $dl18/$bin
    rehash
    docker-compose version # doit afficher 1.8

# run the pod test environment

as declared in `docker-compose.yml:/services/elasticsearch/volumes`,
the `/code` volume is used to share the pod server in the code.

    volumes:
        - ./code:/code

data and logs are used by the vm itself. so to build the env:

    ln -s $PWD/../../../pod_project(:A) code
    mkdir -p data logs media
    docker-compose build

to run it:

    docker-compose up

enter in running vms :

    docker-compose exec [pod|elasticsearch] a command with parameters

prepare the db and the es:

    docker-compose exec python manage.py makemigrations
    docker-compose exec python manage.py migrate
    docker-compose exec python manage.py loaddata core/fixtures/initial_data.json
    docker-compose exec python manage.py createsuperuser --username mylogincas
    docker-compose exec python manage.py create_pod_index
    docker-compose exec python manage.py index_videos __ALL__

execute celery with the following command:

    docker-compose exec pod celery -A pod_project worker -l info

the application is available here:

    http://127.0.0.1:8010/

you can read the following file for more information :
`../../../README_UNISTRA.rst`.
