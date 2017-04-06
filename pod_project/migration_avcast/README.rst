Importation des enregistrements d'audiovideocast
================================================

Cette application permet l'importation des cours d'audiovideocast vers pod.

Attention, il faut que la base de données de pod soit vide au préalable.
En effet, les *id* des cours avcast vont correspondre aux *id* des vidéos pod.
Donc, si des vidéos sont déjà présentes dans pod, il y aura des conflits à l'importation.

L'importation des médias se base sur le mediatype d'avcast, donc celui-ci doit être juste pour
chaque vidéo dans avcast.

Installation
------------

* Mettez ce répertoire dans le dossier *pod_project*.
* Modifiez vos settings de la manière suivante : ::

    INSTALLED_APPS += ('migration_avcast',)
    AVCAST_DB_URI = "host=localhost port=5432 dbname=univrav user=myuser password=S3CR3T"
    AVCAST_COURSE_DEFAULT_USERNAME = "mydefaultuser"
    AVCAST_VOLUME_PATH = "/audiovideocours/cours/1"
    AVCAST_COPY_MODES_LIST = ["FAKE", "LINK", "COPY"]
    AVCAST_COPY_MODE = environ.get("AVCAST_COPY_MODE", AVCAST_COPY_MODES_LIST[0])
    CURSUS_CODES = (
        ("0", "Autres"),
        ("C", "Conférence"),
        ("1", "Licence 1ère année"),
        ("2", "Licence 2ème année"),
        ("3", "Licence 3ème année"),
        ("4", "Master 1ère année"),
        ("5", "Master 2ème année"),
        ("6", "Doctorat")
    )

* Quelques explications des paramètres:

  * **AVCAST_DB_URI** est l'URI de connection à la base de données postgresql d'avcast.
  * **AVCAST_COURSE_DEFAULT_USERNAME** est l'utilisateur utilisé par défaut pour les anciens
    cours qui ne sont pas rattachés à un utilisateur. Cet utilisateur doit bien évidemment exister
    dans pod après la migration des utilisateurs.
  * **AVCAST_COPY_MODE** doit prendre au choix une des valeurs suivantes:

    * **FAKE**: simuler la copie de fichiers lors de l'exécution du script *import_avcast_files*.
    * **LINK**: créer des liens symboliques à la place de copier les fichiers.
    * **COPY**: copier réellement les fichiers.
  * Les titres des **CURSUS_CODES** doivent correspondre aux niveaux dans avcast.

* Exécutez les commandes dans l'ordre suivant : ::

    python manage.py import_avcast_users
    python manage.py import_avcast_amphis
    python manage.py import_avcast_disciplines
    python manage.py import_avcast_courses
    python manage.py import_avcast_files

* Désormais, dans pod, vous devriez avoir :

  * Les utilisateurs d'avcast avec leurs profiles.
  * Les bâtiments et les amphis pour le live.
  * Les disciplines et composantes avcast en tant que chaînes et thèmes dans pod.
  * Les cours avec leurs fichiers, leurs tags, leurs cursus, leurs contributeurs et autres.

* Remarques:

  * Pour les cours client de type *audio*, on importe le *videoslide*.
  * Pour les cours client de type *video*, on importe le *videoslide* en tant que média principal
    et on ajoute la vidéo simple en tant qu'enrichissement.
  * Pour les uploads de type *audio*, on importe le *mp3*.
  * Pour les uploads de type *vidéo*, on import le *mp4*.
  * Cela signifie que le mediatype *html5* ou *hq* est obligatoire pour les vidéos.
    Il faut obligatoirement un fichier *mp4*, car les *flv* ne seront pas pris en compte.
  * S'il y a une vidéo additionnelle, elle est prioritaire à l'importation.
  * Les documents complémentaires sont également récupérés.
  * Mais les sous-titres ne sont pas migrés.
