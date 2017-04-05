# -*- coding: utf-8 -*-

"""
Import all avcast's disciplines in pod's channels and themes
"""
from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import psycopg2
import psycopg2.extras
from pods.models import Discipline, Channel, Theme
from django.template.defaultfilters import slugify

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)


class Command(BaseCommand):
    help = "Import all avcast's disciplines in pod's channels and themes"

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
                        # # create or modify disciplines
                        # discipline, created = Discipline.objects.get_or_create(
                        #     slug=slugify(row['namecomp'])
                        # )
                        # discipline.title = row['namecomp']
                        # discipline.description = "codecomp=%s;codedom=%s;namedom=%s" % (
                        #     row['codecomp'] if row['codecomp'] else "",
                        #     row['codedom'] if row['codedom'] else "",
                        #     row['namedom'] if row['namedom'] else ""
                        # )
                        # discipline.save()
                        # self.stdout.write(self.style.SQL_FIELD('Discipline "%s" saved !' % discipline.title))

                        # create or modify channels
                        channel, created = Channel.objects.get_or_create(
                            slug=slugify(row['namedom'])
                        )
                        channel.title = row['namedom']
                        channel.visible = True
                        channel.description = "codedom=%s" % (
                            row['codedom'] if row['codedom'] else "",
                        )
                        channel.save()
                        self.stdout.write(self.style.SQL_FIELD('Channel "%s" saved !' % channel.title))
                        # create or modify theme
                        theme, created = Theme.objects.get_or_create(
                            slug=slugify(row['namecomp']),
                            channel=channel
                        )
                        theme.title = row['namecomp']
                        theme.description = "codecomp=%s" % (
                            row['codecomp'] if row['codecomp'] else "",
                        )
                        theme.save()
                        self.stdout.write(self.style.SQL_FIELD('Theme "%s" saved !' % channel.title))
        except psycopg2.DatabaseError as e:
            raise e
            raise CommandError("Cannot access to the database ")
        finally:
            if conn:
                conn.close()
                self.stdout.write("Done !")
