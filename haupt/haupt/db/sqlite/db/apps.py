#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
# This file and its contents are licensed under the AGPLv3 License.
# Please see the included NOTICE for copyright information and
# LICENSE-AGPL for a copy of the license.

from django.apps import AppConfig


class DBConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "db.sqlite.db"
    verbose_name = "DB"
