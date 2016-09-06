

# installation des dépendances

TODO: move to the right place

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
   mkdir -p data log
   docker-compose build

to run it:

   docker-compose up

enter in running vms

   docker-compose exec [pod|elasticsearch] a command with parameters

example: show django processes on the pod server

now you can run install and test procedures described in
`../../../README_UNISTRA.rst`.

