# -*- coding: utf-8 -*-

"""
Import all avcast's courses, tags, types in pod
"""

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import psycopg2
import psycopg2.extras
from pods.models import Pod, Type, ContributorPods, Discipline, EncodingPods
from core.models import EncodingType, get_storage_path
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User



# /** media type available **/
# public static final int typeFlash = 1;
# public static final int typeMp3 = 2;
# public static final int typeOgg = 4;
# public static final int typePdf = 8;
# public static final int typeZip = 16;
# public static final int typeVideoslide = 32;
# public static final int typeAdddoc = 64;
# public static final int typeHq = 128;
# public static final int typeVideoslideIpod = 256;
# public static final int typeSubtitles = 512;
# public static final int typeAddVideo = 1024;
# public static final int typeWebm = 2048;
#
#
# /**
#  * Check the media availability
#  * @param type media type(mp3,ogg,...)
#  * @return true if the media is available
#  */
# public boolean isAvailable(String type) {
#         if(type == null || type.equals("")) return false;
#         else if(type.equals("flash")) return ((typeFlash & mediatype) > 0);
#         else if(type.equals("mp3")) return ((typeMp3 & mediatype) > 0);
#         else if(type.equals("ogg")) return ((typeOgg & mediatype) > 0);
#         else if(type.equals("pdf")) return ((typePdf & mediatype) > 0);
#         else if(type.equals("zip")) return ((typeZip & mediatype) > 0);
#         else if(type.equals("videoslide")) return ((typeVideoslide & mediatype) > 0);
#         else if(type.equals("adddoc")) return ((typeAdddoc & mediatype) > 0);
#         else if(type.equals("hq")) return ((typeHq & mediatype) > 0);
#         else if(type.equals("video")) return ((typeHq & mediatype) > 0);
#         else if(type.equals("videoslideipod")) return ((typeVideoslideIpod & mediatype) > 0);
#         else if(type.equals("subtitles")) return ((typeSubtitles & mediatype) > 0);
#         else if(type.equals("addvideo")) return ((typeAddVideo & mediatype) > 0);
#         else if(type.equals("webm")) return ((typeWebm & mediatype) > 0);
#         else if(type.equals("html5")) {
#                 if(this.type.equals("audio"))
#                         return  ((typeMp3 & mediatype) > 0);
#                 else
#                         return ((typeHq & mediatype) > 0) || ((typeWebm & mediatype) > 0);
#         }
#         else return false;
# }
#
#
#














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
                            pod.encoding_status = 'AVCAST'
                            # formation
                            pod = self.pod_add_discipline_and_cursus(conn, pod, row)
                            # Add author and tags
                            pod = self.pod_add_author(pod, row)
                            pod = self.pod_add_tags(conn, pod, row)



                            ###################### TODO créer encodage (mediatype ?)

                            mediatype = row['mediatype']

                            is_videoslide_present = 32 & mediatype > 0
                            is_mp3_present = 2 & mediatype > 0
                            is_videomp4_present = 128 & mediatype > 0
                            is_addvideo_present = 1024 & mediatype > 0

                            # MUA or CA
                            if row['type'] == "audio":
                                # Use the videoslide if he is present (CA)
                                if is_videoslide_present:
                                    file_path = get_storage_path(pod,"%s/%s_videoslide.mp4" % (pod.id, pod.id))
                                    ep, ep_created = EncodingPods.objects.get_or_create(
                                        video=pod,
                                        encodingType=EncodingType.objects.get(name="720"),
                                        encodingFile=file_path,
                                        encodingFormat="video/mp4"
                                    )
                                    pod.video = file_path
                                # TODO else, use mp3 (MUA)
                                elif is_mp3_present:
                                    pass
                                else:
                                    raise CommandError("No media for %s" % pod.id)
                            # MUV or CV or CSC
                            else:
                                # TODO Use the videoslide if he is present (CV)
                                if is_videoslide_present:
                                    pass
                                # TODO priority to additional video
                                elif is_addvideo_present:
                                    pass
                                # TODO else, use mp4 (MUV or CSC)
                                elif is_videomp4_present:
                                    pass
                                elif is_mp3_present:
                                    pass
                                else:
                                    raise CommandError("No media for %s" % pod.id)


                            # encodingpods, ep_created = EncodingPods.objects.get_or_create(
                            #     video=pod,
                            #     encodingType=None,
                            #     encodingFile=None,
                            #     encodingFormat=None
                            #
                            # )



                            ##################################


                            # TODO adddocname => il faut créer un document avec chemin du cours + adddocname dans path
                            is_addoc_present = 64 & mediatype > 0

                            # TODO piste sous titres ? Avcast utilise le format TTML, pod le format WEBVTT
                            is_subtitles_present = 512 & mediatype > 0

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
