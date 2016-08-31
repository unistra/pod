# -*- coding: utf-8 -*-

"""
Import all avcast's buildings and amphis in pod
"""

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import psycopg2
import psycopg2.extras
from pods.models import Recorder, Building


class Command(BaseCommand):
    help = "Import all avcast's buildings and amphis in pod"

    def handle(self, *args, **options):
        # Check settings
        if not hasattr(settings, 'AVCAST_DB_URI') or not settings.AVCAST_DB_URI:
            raise CommandError("AVCAST_DB_URI must be setted")
        self.stdout.write("Import all buildings and amphis ...")
        conn = None
        try:
            conn = psycopg2.connect(settings.AVCAST_DB_URI)
            with conn:
                with conn.cursor(
                    cursor_factory=psycopg2.extras.RealDictCursor
                ) as curs:
                    curs.execute(
                        ('SELECT b.name as bname,a.name as aname,a.ipaddress,'
                         'a.status,a.gmapurl,a.restrictionuds '
                         'FROM amphi a '
                         'INNER JOIN building b '
                         'ON a.buildingid = b.buildingid')
                    )
                    for row in curs.fetchall():
                        # create or modify building
                        building, created = Building.objects.get_or_create(
                            name=row['bname']
                        )

                        # create or modify amphi
                        recorder, created = Recorder.objects.get_or_create(
                            name=row['aname'],
                            building=building,
                            adress_ip=row['ipaddress']
                        )
                        recorder.status = row['status'],
                        recorder.gmapurl = row['gmapurl']
                        recorder.is_restricted = row['restrictionuds']
                        recorder.save()

        except psycopg2.DatabaseError as e:
            raise e
            raise CommandError("Cannot access to the database ")
        finally:
            if conn:
                conn.close()
                self.stdout.write("Done !")
