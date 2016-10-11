# -*- coding: utf-8 -*-

"""
Import all avcast's disciplines in pod
"""
from __future__ import unicode_literals
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
        self.stdout.write("Import all disciplines ...")
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
                            slug=slugify(row['namecomp'].decode('utf-8'))
                        )
                        discipline.title = row['namecomp'].decode('utf-8')
                        discipline.description = "codecomp=%s;codedom=%s;namedom=%s" % (
                            row['codecomp'].decode('utf-8') if row['codecomp'] else "",
                            row['codedom'].decode('utf-8') if row['codedom'] else "",
                            row['namedom'].decode('utf-8') if row['namedom'] else ""
                        )
                        discipline.save()
                        self.stdout.write(self.style.SQL_FIELD('Discipline "%s" saved !' % discipline.title))
        except psycopg2.DatabaseError as e:
            raise e
            raise CommandError("Cannot access to the database ")
        finally:
            if conn:
                conn.close()
                self.stdout.write("Done !")
