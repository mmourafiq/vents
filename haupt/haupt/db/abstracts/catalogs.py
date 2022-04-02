#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
# This file and its contents are licensed under the AGPLv3 License.
# Please see the included NOTICE for copyright information and
# LICENSE-AGPL for a copy of the license.

from django.db import models

from db.abstracts.describable import DescribableModel
from db.abstracts.diff import DiffModel
from db.abstracts.live_state import LiveStateModel
from db.abstracts.nameable import RequiredNameableModel
from db.abstracts.tag import TagModel
from db.abstracts.uid import UuidModel


class BaseCatalog(
    UuidModel,
    RequiredNameableModel,
    DiffModel,
    DescribableModel,
    TagModel,
):
    class Meta:
        abstract = True
        indexes = [models.Index(fields=["name"])]


class BaseLiveStateCatalog(
    BaseCatalog,
    LiveStateModel,
):
    class Meta:
        abstract = True
        indexes = [models.Index(fields=["name"])]
