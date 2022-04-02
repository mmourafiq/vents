#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
# This file and its contents are licensed under the AGPLv3 License.
# Please see the included NOTICE for copyright information and
# LICENSE-AGPL for a copy of the license.


from django.db import migrations, models


def migrate_runtime(apps, schema_editor):
    Run = apps.get_model("db", "Run")

    runs = []
    for r in Run.objects.all():
        r.runtime = r.meta_info.pop("meta_kind", None)
        runs.append(r)

    Run.objects.bulk_update(runs, ["meta_info", "runtime"])


class Migration(migrations.Migration):

    dependencies = [
        ("db", "0005_auto_20201005_0913"),
    ]

    operations = [
        migrations.AddField(
            model_name="run",
            name="runtime",
            field=models.CharField(blank=True, db_index=True, max_length=12, null=True),
        ),
        migrations.RunPython(migrate_runtime),
    ]
