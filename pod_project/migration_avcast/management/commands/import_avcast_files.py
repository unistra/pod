# -*- coding: utf-8 -*-

"""
Import files
"""

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from pods.models import Pod
import os


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

    def handle(self, *args, **options):
        # TODO work in progress
        begin = options['begin']
        end = options['end']

        if not hasattr(settings, 'AVCAST_VOLUME_PATH') or not settings.AVCAST_VOLUME_PATH:
            raise CommandError("AVCAST_VOLUME_PATH must be setted")

        try:
            self.stdout.write("Import all files ...")
            # Get imported Pods form avcast
            list_pods = Pod.objects.filter(
                encoding_status="AVCAST",
                id__gte=begin,
                id__lte=end)

            # TODO mv files from EncodingPods
            for pod in list_pods:
                self.stdout.write("Processing %s" % pod)
                for encodingpod in pod.encodingpods_set.all():
                    filename = os.path.basename(encodingpod.encodingFile.name)
                    mediafolder = self.avcast_get_media_folder(
                        pod.id, settings.AVCAST_VOLUME_PATH)
                    origin = os.path.join(mediafolder, filename)
                    destination = encodingpod.encodingFile.path
                    self.stdout.write("From %s to %s" % (origin, destination))

            # TODO mv files from DocPods
            # TODO mv files from TrackPods ???

        except:
            raise CommandError("An error occurs")
        finally:
            self.stdout.write("Done !")
