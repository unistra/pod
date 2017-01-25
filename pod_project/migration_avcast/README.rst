Importation des enregistrements d'audiovideocast
================================================

* Modifiez vos settings de la manière suivante : ::

    INSTALLED_APPS += ('migration_avcast',)
    AVCAST_DB_URI = "host=localhost port=5432 dbname=univrav user=myuser password=S3CR3T"
    AVCAST_COURSE_DEFAULT_USERNAME = "mydefaultuser"
    AVCAST_VOLUME_PATH = "/audiovideocours/cours/1"
    AVCAST_FAKE_FILES_COPY = "False"

* Exécutez les commandes dans l'ordre suivant : ::

    python manage.py import_avcast_users
    python manage.py import_avcast_amphis
    python manage.py import_avcast_disciplines
    python manage.py import_avcast_courses
    python manage.py import_avcast_files
