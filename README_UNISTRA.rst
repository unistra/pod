Installation de la plate-forme Pod à l'Université de Strasbourg
===============================================================

Bienvenue sur `la plate-forme Pod de l'Université de Strasbourg <https://github.com/unistra/pod>`_,
qui est un fork du `projet de l'Université de Lille <https://github.com/EsupPortail/pod>`_.

La branche **master** est conforme à la branche **master** de dépôt d'origine.
Celle-ci ne devra pas être modifiée et servira à récupérer les commits du dépôt
d'origine.

La branche **unistra** contient le paramétrage de la configuration de l'Unistra.
Ce paramétrage django s'inspire du `template django-drybones <https://github.com/unistra/django-drybones>`_
et permet de déployer l'application via `pydiploy <https://github.com/unistra/pydiploy>`_ et d'exécuter
les tests unitaires via `tox <https://testrun.org/tox/latest/>`_.

Les fichiers et dossiers spécifiques liés à cette version sont les suivants:

* Ce fichier **README_UNISTRA.rst**
* Le dossier **pod_project/requirements** qui contient l'ensemble des dépendances python, inspiré du fichier racine **requirements.txt**:

  * **common.txt**: Contient les packages communs aux différents environnements
  * **dev.txt**: Contient en plus les packages spécifiques au développement (coverage, tox)
  * **test.txt**: Contient en plus les packages spécifiques à l'environnement de test (psycopg2, chaussette, waitress)
  * **preprod.txt**: Contient en plus les packages spécifiques à l'environnement de pre-production (psycopg2, chaussette, waitress)
  * **prod.txt**: Contient en plus les packages spécifiques à l'environnement de prod (psycopg2, chaussette, waitress)

* Le fichier **pod_project/manage.py** qui est le template de management de django pour pydiploy, librairie basée sur `fabric <http://www.fabfile.org/>`_
* Le fichier **pod_project/requirements.txt** qui dépend du dossier **pod_project/requirements**
* Le dossier **pod_project/fabfile** qui est le fichier de configuration de pydiploy
* Le fichier **pod_project/nginx_with_load_balancer.patch** qui est une modification de la conf nginx pour la prod et la preprod (avec load balancer)
* Le fichier **pod_project/MANIFEST.in** qui permet d'inclure certains fichiers dans le package python
* Le fichier **setup.py** qui permet de packager l'application, nécessaire à tox
* Le fichier **tox.ini** qui permet d'exécuter les tests unitaires sous différents environnements
* Le fichier **pod_project/pod_project/wsgi.py** qui est un template pour pydiploy permettant l'utilisation d'un serveur wsgi
* Le dossier **pod_project/pod_project/settings**, qui contient l'ensemble des fichiers de configuration pour les différents environnements:
* Le dossier **pod_project/elasticsearch**, qui contient la configuration d'elasticsearch pour tox
* Le fichier **pod_project/pod_project/urls.py**, qui contient la configuration d'elasticsearch pour tox

  * **base.py**: Contient les paramètres communs. C'est une copie exacte du fichier **settings-sample.py**
  * **dev.py**: Contient la configuration de l'environnement de développement
  * **test.py**: Contient la configuration de l'environnement de test
  * **preprod.py**: Contient la configuration de l'environnement de pre-production
  * **prod.py**: Contient la configuration de l'environnement de production

Etant donné que cette configuration spécifique est principalement basée sur de l'ajout de fichiers, et non pas de la modification de fichiers, il
sera assez simple de merger les commits du dépôt source depuis la branche master.

Dans le cas d'un pull request d'une fonctionnalité, il faudra:

* Effectuer les modifications du code dans la branche unistra en ajoutant des tests unitaires. Le commit devra être propre, ne concerner qu'une seule fonctionnalité,
  et fonctionner sur le dépôt distant
* Synchroniser master avec le master distant, forker la branch master dans une branche qui respecte la convention de nommage du dépôt d'origine (ex: dotmobo/bugfix-correct_unit_tests)
* Utiliser git cherry pick pour n'appliquer que le commit de la fonctionnalité dans cette branche
* Faire le pull request de cette branche

Développement
-------------

* Utiliser docker-compose dans eg/docker
* On utilise sqlite en dev.

Installation en prod
--------------------

* Préparer une machine virtuelle Ubuntu 16.04
* Pour test, preprod et prod, créer une base de données postgresql vide.
* Installer manuellement Elasticsearch 2:

  * apt-get install openjdk-8-jre-headless
  * wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
  * echo "deb https://packages.elastic.co/elasticsearch/2.x/debian stable main" | sudo tee -a /etc/apt/sources.list.d/elasticsearch-2.x.list
  * sudo apt-get update && sudo apt-get install elasticsearch
  * sudo update-rc.d elasticsearch defaults 95 10

* Configurer elasticsearch dans /etc/elasticsearch/elasticsearch.yml : ::

        #POD
        cluster.name: pod
        node.name: Pod1
        network.host: 127.0.0.1
        discovery.zen.ping.multicast.enabled: false
        discovery.zen.ping.unicast.hosts: ["127.0.0.1"]

* Configurer rabbitmq à l'aide du script dans eg/rabbitmq

* Préparer l'environnement python via pydiploy : **fab prod pre_install**

* Créer le répertoire des médias : mkdir -p /nfs/media/pod && chown -R django:di /nfs/media
* Créer le répertoire temporaire pour l'upload nginx : mkdir -p /nfs/tmp/django && chown -R django:di /nfs/tmp
* Créer le répertoire temporaire pour l'upload django : mkdir -p /nfs/tmp/nginx && chown -R django:di /nfs/tmp

* Déployer le code de la branche **unistra** via pydiploy: **fab tag:unistra prod deploy --set default_db_host=X,default_db_user=X,
  default_db_password=X,default_db_name=X,cas_server_url=X,auth_ldap_server_uri=X,auth_ldap_bind_dn=X,auth_ldap_bind_password=X,
  auth_ldap_base_dn=X,avcast_db_uri=X,celery_broker=X**
* Pour les déploiements suivant, un **fab tag:unistra prod deploy** suffira
* Finir la configuration via pydiploy: **fab prod post_install**

Il reste encore du paramétrage manuel à faire. A voir pour l'automatiser plus tard.
On peut utiliser pour l'instant pydiploy via **fab prod custom_manage_cmd:ma_commande**:

* **python manage.py makemigrations** && **python manage.py migrate**
* **python manage.py loaddata core/fixtures/initial_data.json**
* **python manage.py createsuperuser --username root**

Concernant elasticsearch:

* dans l'interfaçe d'admin de pod, il faut modifier l'url qui est dans Sites
* dans l'interface d'admin, modifier la page statique "/" et ajouter la page statique "/unistra-mentionslegales/", en utilisant le template "default.html"
* si l'index pod existe déjà : **curl -XDELETE 'http://localhost:9200/pod/'**
* **python manage.py create_pod_index**
* si des vidéos sont déjà présentes : **python manage.py index_videos __ALL__**

Pour lancer les tests unitaires :

* Il faut installer **docker** au préalable pour utiliser un elasticsearch dans
  les tests
* Puis, exécuter la commande **tox**

Astuces : 

* Si vous utilisez des "username" supérieurs à 30 caractères, n'hésitez pas à augmenter la limite de la table auth_user en base.

TODO
----

* Paramétrer le dossier MEDIA_ROOT et l'url /media dans pydiploy/nginx
* Env de dev version beta quasiment ok. A voir pour test, preprod et prod.
* Automatiser l'installation d'Elasticsearch
* Automatiser l'installation de Ffmpeg
* Automatiser l'exécution des commandes django annexes (loaddata,makemigrations ...)

ENCODE_VIDEO
------------

dans les settings, creer une clef ENCODE_VIDEO qui référence la fonction a appeller. exemple
dans settings/devhpc.py.

Celery
------
Les 3 paramètres du fichier de configuration concernés sont donc:

* Pour activer l'encodage via Celery dans settings

    from pod_project.tasks import task_start_encode

    def encode_video(video):
            task_start_encode.delay(instance)
    
    ENCODE_VIDEO = encode_video

 M pod_project/pods/models.py
?? pod_project/pod_project/settings/devhpc.py



* Pour définir le nom du projet (ne devrait pas changer) : CELERY_NAME = "pod_project"
* Pour définir le type de backend (ici rabbitmq) : CELERY_BACKEND = "amqp"
* Pour définir le broker (ici un rabbitmq local) : CELERY_BROKER = "amqp://guest@localhost//"

Au niveau du backend et du broker, il est également possible d'utiliser redis par exemple.

Pour exécuter Celery manuellement, il suffit d'exécuter la commande dans le répertoire du projet:
*celery -A pod_project worker -l info*

Il est également possible de démarrer celery via systemd ou init (http://docs.celeryproject.org/en/3.1/tutorials/daemonizing.html)

Pour lancer l'encodage sur d'autres serveurs, il faut pour chaque serveur d'encodage

Déployer le code de l'application (mais sans lancer le serveur wsgi)
Exécuter celery via systemd ou init
Les différents serveurs se débrouillent pour se répartir la charge via rabbitmq
A titre informatif, voici notre fichier de configuration Celery pour la séparation de l'encodage, à adapter évidemment (/etc/default/celery)

    CELERYD_NODES="worker1"
    DJANGO_SETTINGS_MODULE="pod_project.settings.preprod"
    CELERY_BIN="/home/django/.virtualenvs/pod/bin/celery"
    CELERY_APP="pod_project"
    CELERYD_CHDIR="/home/django/podcast-pprd.unistra.fr/current"
    CELERYD_OPTS="--time-limit=86400 --concurrency=1 --maxtasksperchild=1"
    CELERYD_LOG_FILE="/var/log/celery/%N.log"
    CELERYD_PID_FILE="/var/run/celery/%N.pid"
    CELERYD_USER="django"
    CELERYD_GROUP="di"
    CELERY_CREATE_DIRS=1
    CELERYD_LOG_LEVEL="INFO"

Les CPU des serveurs web ne sont ainsi plus surchargés par ffmpeg.
On peut facilement rajouter des workers Celery si on a besoin de plus de machine d'encodage.

Du coup, on a le fonctionnement suivant en preprod :

* un serveur rabbitmq pour gérer la file d'attente des jobs
* 2 serveurs web qui servent l'application et qui crééent les jobs dans rabbitmq via le client celery
* 2 serveurs d'encodage qui écoutent la file d'attente via les workers celery et qui lancent les jobs
