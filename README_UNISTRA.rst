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

* Le dossier **pod_project/locale** qui contient les locales FR inspiré du dossier racine **traduction**
* Le fichier **pod_project/manage.py** qui est le template de management de django pour pydiploy, librairie basée sur `fabric <http://www.fabfile.org/>`_
* Le fichier **pod_project/requirements.txt** qui dépend du dossier **pod_project/requirements**
* Le fichier **pod_project/fabfile.py** qui est le fichier de configuration de pydiploy
* Le fichier **pod_project/nginx_with_load_balancer.patch** qui est une modification de la conf nginx pour la prod et la preprod (avec load balancer)  
* Le fichier **pod_project/MANIFEST.in** qui permet d'inclure certains fichiers dans le package python
* Le fichier **setup.py** qui permet de packager l'application, nécessaire à tox
* Le fichier **tox.ini** qui permet d'exécuter les tests unitaires sous différents environnements
* Le fichier **pod_project/pod_project/wsgi.py** qui est un template pour pydiploy permettant l'utilisation d'un serveur wsgi
* Le dossier **pod_project/pod_project/settings**, qui contient l'ensemble des fichiers de configuration pour les différents environnements:
* Le dossier **pod_project/elasticsearch**, qui contient la configuration d'elasticsearch pour tox  

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

Installation
------------

* Préparer une machine virtuelle Ubuntu 14.04
* Pour test, preprod et prod, créer une base de données postgresql vide. On utilise sqlite en dev.
* Installer manuellement Elasticsearch 1.6:

  * apt-get install openjdk-7-jre-headless
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

* Installer manuellement ffmpeg:

  * cd /usr/local/
  * wget http://johnvansickle.com/ffmpeg/releases/ffmpeg-release-64bit-static.tar.xz
  * tar -Jxvf ffmpeg-release-64bit-static.tar.xz
  * rm ffmpeg-release-64bit-static.tar.xz
  * mv ffmpeg-X.X.X-64bit-static ffmpeg
  * ln -s /usr/local/ffmpeg/ffmpeg /usr/local/bin/ffmpeg
  * ln -s /usr/local/ffmpeg/ffmpeg-10bit /usr/local/bin/ffmpeg-10bit
  * ln -s /usr/local/ffmpeg/ffprobe /usr/local/bin/ffprobe
  * ln -s /usr/local/ffmpeg/ffserver /usr/local/bin/ffserver
  * ln -s /usr/local/ffmpeg/qt-faststart /usr/local/bin/qt-faststart

* Créer le répertoire des médias : mkdir -p /srv/media/pod && chown -R django:di /srv/media
* Préparer l'environnement python via pydiploy : **fab prod pre_install**
* Déployer le code de la branche **unistra** via pydiploy: **fab tag:unistra prod deploy --set default_db_host=X,default_db_user=X,default_db_password=X,default_db_name=X,cas_server_url=X,auth_ldap_server_uri=X,auth_ldap_bind_dn=X,auth_ldap_bind_password=X,auth_ldap_base_dn=X**
* Finir la configuration via pydiploy: **fab prod post_install**

Il reste encore du paramétrage manuel à faire. A voir pour l'automatiser plus tard.
On peut utiliser pour l'instant pydiploy via **fab prod custom_manage_cmd:ma_commande**:

* **python manage.py makemigrations** && **python manage.py migrate**
* **python manage.py loaddata core/fixtures/initial_data.json**
* **python manage.py createsuperuser --username root**

Concernant elasticsearch:

* dans l'interfaçe d'admin de pod, il faut modifier l'url qui est dans Sites
* si l'index pod existe déjà : **curl -XDELETE 'http://localhost:9200/pod/'**
* **python manage.py create_pod_index**
* si des vidéos sont déjà présentes : **python manage.py index_videos __ALL__**

Pour lancer les tests unitaires :

* Il faut installer **docker** au préalable pour utiliser un elasticsearch dans
  les tests
* Puis, exécuter la commande **tox**

TODO
----

* Paramétrer le dossier MEDIA_ROOT et l'url /media dans pydiploy/nginx
* Env de dev version beta quasiment ok. A voir pour test, preprod et prod.
* Automatiser l'installation d'Elasticsearch
* Automatiser l'installation de Ffmpeg
* Automatiser l'exécution des commandes django annexes (loaddata,makemigrations ...)
