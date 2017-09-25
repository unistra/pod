# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pods', '0016_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pod',
            name='cursus',
            field=models.CharField(default='0', max_length=1, choices=[(b'0', b'Autres'), (b'C', b'Conf\xc3\xa9rence'), (b'D', b'Dipl\xc3\xb4me universitaire'), (b'1', b'Licence 1\xc3\xa8re ann\xc3\xa9e'), (b'2', b'Licence 2\xc3\xa8me ann\xc3\xa9e'), (b'3', b'Licence 3\xc3\xa8me ann\xc3\xa9e'), (b'4', b'Master 1\xc3\xa8re ann\xc3\xa9e'), (b'5', b'Master 2\xc3\xa8me ann\xc3\xa9e'), (b'6', b'Doctorat')], verbose_name='University course'),
        ),
    ]
