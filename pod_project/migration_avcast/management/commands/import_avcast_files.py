# -*- coding: utf-8 -*-

"""
Import files
"""
from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from pods.models import Pod
import os
import shutil
import filecmp


class Command(BaseCommand):
    help = "Import all avcast's files in pod"

    def add_arguments(self, parser):
        parser.add_argument('begin', nargs='?', type=int, default=1)
        parser.add_argument('end', nargs='?', type=int, default=2147483647)

    def avcast_get_media_folder(self, courseid, volume_path):
        idformat = "%08d" % courseid
        if len(idformat) <= 8:
            mediafolder = os.path.join(volume_path, idformat[0:2],
                idformat[2:4], idformat[4:6], idformat[6:8])
        else:
            mediafolder = os.path.join(volume_path, courseid)
        return mediafolder

    def pod_processing_encodingpods(self, pod):
        for encodingpod in pod.encodingpods_set.all():
            filename = os.path.basename(encodingpod.encodingFile.name)
            mediafolder = self.avcast_get_media_folder(
                pod.id, settings.AVCAST_VOLUME_PATH)
            if "addvideo" in filename:
                origin = os.path.join(mediafolder, "additional_video", filename)
            else:
                origin = os.path.join(mediafolder, filename)
            destination = encodingpod.encodingFile.path
            self.stdout.write("---- Check encoding pod : From %s to %s" % (origin, destination))
            self.pod_copy_file(origin, destination)

    def pod_processing_docpods(self, pod):
        for docpod in pod.docpods_set.all():
            if docpod.document.original_filename:
                filename = docpod.document.original_filename
            else:
                filename = os.path.basename(docpod.document.file.name)
            mediafolder = self.avcast_get_media_folder(
                pod.id, settings.AVCAST_VOLUME_PATH)
            origin = os.path.join(mediafolder, "additional_docs", filename)
            destination = docpod.document.file.path
            self.stdout.write("---- Check doc pod : From %s to %s" % (origin, destination))
            self.pod_copy_file(origin, destination)

    def pod_processing_enrichpods(self, pod):
        for enrichpod in pod.enrichpods_set.all():
            filename = os.path.basename(enrichpod.document.file.name)
            mediafolder = self.avcast_get_media_folder(
                pod.id, settings.AVCAST_VOLUME_PATH)
            if "addvideo" in filename:
                origin = os.path.join(mediafolder, "additional_video", filename)
            else:
                origin = os.path.join(mediafolder, filename)
            destination = enrichpod.document.file.path
            self.stdout.write("---- Check enrich pod : From %s to %s" % (origin, destination))
            self.pod_copy_file(origin, destination)

    def pod_copy_file(self, origin, destination):
            # on affiche un warning si le fichier origin n'existe pas et on continue la boucle
            if not os.path.isfile(origin):
                self.stderr.write(self.style.WARNING("------ Warning : The file %s doesn't exist !" % origin))
            else:
                # create destination folder
                pod_folder = os.path.dirname(destination)
                if not os.path.exists(pod_folder):
                    if settings.AVCAST_COPY_MODE == "COPY":
                        os.makedirs(pod_folder)
                        self.stdout.write(self.style.SQL_FIELD("------ Folder %s created" % pod_folder))
                    elif settings.AVCAST_COPY_MODE == "LINK":
                        os.makedirs(pod_folder)
                        self.stdout.write(self.style.SQL_FIELD("------ Folder %s created" % pod_folder))
                    else:
                        self.stdout.write(self.style.SQL_FIELD("------ Fake : Folder %s created" % pod_folder))
                # copy the file if he doesn't exist or if he's different
                if not os.path.isfile(destination) or not filecmp.cmp(origin, destination):
                    if settings.AVCAST_COPY_MODE == "COPY":
                        shutil.copy2(origin, destination)
                        self.stdout.write(self.style.SQL_FIELD("------ File %s copied to %s" % (origin, destination)))
                    elif settings.AVCAST_COPY_MODE == "LINK":
                        os.symlink(origin, destination)
                        self.stdout.write(self.style.SQL_FIELD("------ File %s linked to %s" % (origin, destination)))
                    else:
                        self.stdout.write(self.style.SQL_FIELD("------ Fake : File %s copied to %s" % (origin, destination)))

    def handle(self, *args, **options):
        begin = options['begin']
        end = options['end']
        # Check settings
        if not hasattr(settings, 'AVCAST_VOLUME_PATH') or not settings.AVCAST_VOLUME_PATH:
            raise CommandError("AVCAST_VOLUME_PATH must be setted")
        if not hasattr(settings, 'AVCAST_COPY_MODE'):
            raise CommandError("AVCAST_COPY_MODE must be setted")

        try:
            self.stdout.write("Import all files ...")
            # Get imported Pods form avcast
            list_pods = Pod.objects.filter(
                encoding_status="AVCAST",
                id__gte=begin,
                id__lte=end)

            for pod in list_pods:
                self.stdout.write("-- Processing %s" % pod)
                self.pod_processing_encodingpods(pod)
                self.pod_processing_docpods(pod)
                self.pod_processing_enrichpods(pod)

        except Exception as e:
            raise CommandError("An error occurs", e)
        finally:
            self.stdout.write("Done !")
