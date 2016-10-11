# -*- coding: utf-8 -*-

"""
Import all avcast's disciplines in pod
"""

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import psycopg2
import psycopg2.extras
from pods.models import Discipline
from django.template.defaultfilters import slugify


class Command(BaseCommand):
    help = "Import all avcast's disciplines in pod"

    def handle(self, *args, **options):
        # Check settings
        if not hasattr(settings, 'AVCAST_DB_URI') or not settings.AVCAST_DB_URI:
            raise CommandError("AVCAST_DB_URI must be setted")
        self.stdout.write(u"Import all disciplines ...")
        conn = None
        try:
            conn = psycopg2.connect(settings.AVCAST_DB_URI)
            with conn:
                with conn.cursor(
                    cursor_factory=psycopg2.extras.RealDictCursor
                ) as curs:
                    curs.execute(
                        ('SELECT * '
                         'FROM discipline')
                    )
                    for row in curs.fetchall():
                        # create or modify disciplines
                        discipline, created = Discipline.objects.get_or_create(
                            slug=slugify(row['namecomp'])
                        )
                        discipline.title = row['namecomp']
                        discipline.description = "codecomp=%s;codedom=%s;namedom=%s" % (
                            row['codecomp'],
                            row['codedom'],
                            row['namedom']
                        )
                        discipline.save()
                        self.stdout.write(self.style.SQL_FIELD(u'Discipline "%s" saved !' % discipline.title.decode('utf-8')))
        except psycopg2.DatabaseError as e:
            raise e
            raise CommandError("Cannot access to the database ")
        finally:
            if conn:
                conn.close()
                self.stdout.write(u"Done !")
