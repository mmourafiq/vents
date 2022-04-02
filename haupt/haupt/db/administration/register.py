#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
# This file and its contents are licensed under the AGPLv3 License.
# Please see the included NOTICE for copyright information and
# LICENSE-AGPL for a copy of the license.

from django.contrib.admin import site
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from db.abstracts.getter import get_artifact_model, get_project_model, get_run_model
from db.administration.artifacts import ArtifactAdmin
from db.administration.projects import ProjectAdmin
from db.administration.runs import RunLightAdmin

site.register(get_user_model(), UserAdmin)
site.register(get_artifact_model(), ArtifactAdmin)
site.register(get_project_model(), ProjectAdmin)
site.register(get_run_model(), RunLightAdmin)
