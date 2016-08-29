# -*- coding: utf-8 -*-

"""
Import all avcast's courses, tags, types in pod
"""

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import psycopg2
import psycopg2.extras
from pods.models import Pod, Type, ContributorPods, Discipline
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Import all avcast's courses, tags, types in pod"

    def add_arguments(self, parser):
        parser.add_argument('begin', nargs='?', type=int)
        parser.add_argument('end', nargs='?', type=int)
        parser.add_argument('--update_sequence',
            dest='update_sequence', action='store_true')
        parser.add_argument('--no-update_sequence',
            dest='update_sequence', action='store_false')
        parser.set_defaults(update_sequence=False)

    def pod_add_author(self, pod, row):
        """ Method to add an author in the contributors list """
        if row['name'] or row['firstname']:
            ContributorPods.objects.get_or_create(
                video=pod,
                name=" ".join([
                    row['name'] if row['name'] else '',
                    row['firstname'] if row['firstname'] else ''
                ]),
                role="author"
            )
        return pod

    def pod_add_tags(self, conn, pod, row):
        """ Method to add tags to pod """
        # add tags
        pod.tags.clear()
        with conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        ) as curs_tags:
            curs_tags.execute(
                ('SELECT tag, courseid '
                 'FROM tag c '
                 'WHERE courseid = ' + str(row['courseid']))
            )
            for row_tag in curs_tags.fetchall():
                if row_tag['tag']:
                    pod.tags.add(row_tag['tag'])
        return pod

    def pod_alter_pod_sequence(self, conn, last_courseid):
        """ Method to alter pod sequence for postgresql """
        with conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        ) as curs_podid:
            try:
                curs_podid.execute("SELECT setval('pods_pod_id_seq', %s)" % last_courseid)
            except Exception:
                self.stdout.write("Warning : cannot change pod id sequence (maybe you don't use postgresql ...)")

    def pod_add_discipline_and_cursus(self, conn, pod, row):
        """ Method to add discipline and cursus to pod """
        with conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        ) as curs_form:
            curs_form.execute(
                ("SELECT c.courseid, c.formation, d.codecomp, d.namecomp, l.code, l.name "
                 "FROM course c "
                 "LEFT JOIN discipline d "
                 "ON c.formation like '%' || d.codecomp || '-%' "
                 "LEFT JOIN level l "
                 "ON c.formation like '%-' || l.code || '%' "
                 "WHERE c.courseid = " + str(row['courseid']))
            )
            row_formation = curs_form.fetchone()
            if row_formation:
                try:
                    # Discipline
                    discipline = Discipline.objects.get(
                        slug=slugify(row_formation['namecomp'])
                    )
                    pod.discipline = [discipline]
                    # Cursus
                    for cursus in settings.CURSUS_CODES:
                        if cursus[1] == row_formation['name']:
                            pod.cursus = cursus[0]
                            break
                    if not pod.cursus:
                        # it shouldn't happen. Set CURSUS_CODES first
                        raise CommandError("Cursus of course %s not found" % row['courseid'])
                except:
                    # it shouldn't happen. Import discipline first
                    raise CommandError("Discipline of course %s not found" % row['courseid'])
            else:
                # it shouldn't happen
                raise CommandError("Formation of course %s not found" % row['courseid'])
        return pod

    def handle(self, *args, **options):
        self.stdout.write("Import all courses, tags, types ...")
        begin = options['begin'] if 'begin' in options and options['begin'] else 1
        end = options['end'] if 'end' in options and options['end'] else 2147483647
        conn = None
        last_courseid=None
        try:
            conn = psycopg2.connect(settings.AVCAST_DB_URI)
            with conn:
                with conn.cursor(
                    cursor_factory=psycopg2.extras.RealDictCursor
                ) as curs:
                    curs.execute(
                        ('SELECT c.*, u.login '
                         'FROM course c '
                         'LEFT JOIN "user" u '
                         'ON u.userid = c.userid '
                         'WHERE c.courseid >= ' + str(begin) + ' '
                         'AND c.courseid <= ' + str(end))

                    )
                    for row in curs.fetchall():
                        print(row)
                        # Get the user. Launch the import_users script before !
                        try:
                            if not row['login']:
                                owner = User.objects.get(username=settings.AVCAST_COURSE_DEFAULT_USERNAME)
                            else:
                                # TODO which default login ?
                                owner = User.objects.get(username=row['login'])
                        except:
                            # it shouldn't happen
                            raise CommandError("User %s not found" % owner)
                        else:
                            # Get or create type
                            pod_type, pod_type_created = Type.objects.get_or_create(
                                slug=slugify(row['type']), title_fr=row['type'], title_en=row['type'])
                            # Create pod
                            pod, pod_created = Pod.objects.get_or_create(
                                id=row['courseid'],
                                to_encode=False,
                                owner=owner,
                                type=pod_type,
                                title=row['title']
                            )
                            # set the last course id for sequence
                            last_courseid = pod.id
                            # modify data
                            pod.date_added = row['date']
                            pod.description = row['description'] if row['description'] else ''
                            pod.duration = row['duration']
                            pod.password = row['genre']
                            pod.is_draft = not row['visible']
                            pod.view_count = row['consultations']
                            pod.allow_downloading = row['download']
                            pod.is_restricted = row['restrictionuds']
                            pod.date_evt = row['recorddate']
                            # formation
                            pod = self.pod_add_discipline_and_cursus(conn, pod, row)
                            # Add author and tags
                            pod = self.pod_add_author(pod, row)
                            pod = self.pod_add_tags(conn, pod, row)

                            # TODO adddocname => il faut créer un document avec chemin du cours + adddocname dans path

                            # TODO créer encodage (mediatype ?)

                            # TODO piste sous titres ? Avcast utilise le format TTML, pod le format WEBVTT

                            # Save all modification
                            pod.save()

                # Alter pod id sequence for postgresql
                if last_courseid and options["update_sequence"]:
                    self.pod_alter_pod_sequence(conn, last_courseid)


                # TODO export CSV (id avcast, mediatype avcast, id pod, login owner)

        except psycopg2.DatabaseError as e:
            raise CommandError("Cannot access to the database ")
        finally:
            if conn:
                conn.close()
                self.stdout.write("Done !")
