# -*- coding: utf-8 -*-

"""
Import all avcast's users in pod
"""
from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import psycopg2
import psycopg2.extras
from django.contrib.auth.models import User
from core.models import UserProfile


class Command(BaseCommand):
    help = "Import all avcast's users in pod"

    def handle(self, *args, **options):
        # Check settings
        if not hasattr(settings, 'AVCAST_DB_URI') or not settings.AVCAST_DB_URI:
            raise CommandError("AVCAST_DB_URI must be setted")
        self.stdout.write("Import all users ...")
        conn = None
        try:
            conn = psycopg2.connect(settings.AVCAST_DB_URI)
            with conn:
                with conn.cursor(
                    cursor_factory=psycopg2.extras.RealDictCursor
                ) as curs:
                    curs.execute(
                        ('select distinct(u.*) from "user" u '
                         'INNER JOIN course c '
                         'ON u.userid = c.userid')
                    )
                    for row in curs.fetchall():
                        # login is required
                        if not row['login']:
                            raise CommandError("A user has no login !")
                        # create or modify the user
                        user, created = User.objects.get_or_create(
                            username=row['login'].decode('utf-8'))
                        user.email = row['email'].decode('utf-8') if row['email'] else ""
                        user.first_name = row['firstname'].decode('utf-8') if row['firstname'] else ""
                        user.last_name = row['lastname'].decode('utf-8') if row['lastname'] else ""
                        if row['password'] and row["passwordtype"]:
                            user.password = "%s1$$%s" % (row['passwordtype'].decode('utf-8'),
                                                         row['password'].decode('utf-8'))
                        else:
                            user.password = "!%s" % (
                                User.objects.make_random_password())
                        user.is_active = row["activate"] if row["activate"] else False
                        user.is_staff = True if row['profile'] in \
                            ("employee", "faculty") else False
                        user.save()
                        # modify user profile
                        profile, created = UserProfile.objects.get_or_create(
                            user=user)
                        profile.auth_type = "loc." if row['type'] == "local" else "cas"
                        profile.description = "establishment=%s;etp=%s;institute=%s" % \
                            (row['establishment'].decode('utf-8') if row['establishment'] else '',
                             row['etp'].decode('utf-8') if row['etp'] else '',
                             row["institute"].decode('utf-8') if row['institute'] else '')
                        profile.affiliation = row['profile'].decode('utf-8') if row['profile'] else "member"
                        profile.save()
                        self.stdout.write(self.style.SQL_FIELD('User "%s" saved !' % user.username))
        except psycopg2.DatabaseError:
            raise CommandError("Cannot access to the database ")
        finally:
            if conn:
                conn.close()
                self.stdout.write("Done !")
