# -*- coding: utf-8 -*-

"""
Import files
"""

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings



class Command(BaseCommand):
    help = "Import all avcast's files in pod"

    def add_arguments(self, parser):
        parser.add_argument('begin', nargs='?', type=int, default=1)
        parser.add_argument('end', nargs='?', type=int, default=2147483647)

    def handle(self, *args, **options):
        # TODO work in progress
        begin = options['begin']
        end = options['end']
        self.stdout.write("Import all files ...")
        print(begin)
        print(end)
        # Get imported Pods form avcast
        #list_pods = Pods.objects.get(encoding_status="AVCAST")
        #print(list_pods)
