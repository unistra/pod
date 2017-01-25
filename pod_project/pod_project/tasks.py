# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.signals import task_prerun, task_success, task_failure


@shared_task(bind=True)
def task_start_encode(self, video):
    print "START ENCODE VIDEO ID %s" % video.id
    from core.utils import encode_video
    encode_video(video)


# @shared_task(bind=True) # utile pour les "reusable apps"
# def task_generate_archive_files(self, date):
#     """ generate pdf and xml files """
#     get_persons_and_generate_pdfs(date)
#
#
# @task_prerun.connect(sender=task_generate_archive_files)
# def start_generate_archive_files(sender=None, *args, **kwargs):
#     print("Initialisation du statut du lot en base")
#
#
# @task_success.connect(sender=task_generate_archive_files)
# def success_generate_archive_files(sender=None, *args, **kwargs):
#     print("Modification du statut du lot en réussi")
#
#
# @task_failure.connect(sender=task_generate_archive_files)
# def failure_generate_archive_files(sender=None, *args, **kwargs):
#     print("Modification du statut du lot en échec")
