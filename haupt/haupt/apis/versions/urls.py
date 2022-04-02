#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
# This file and its contents are licensed under the AGPLv3 License.
# Please see the included NOTICE for copyright information and
# LICENSE-AGPL for a copy of the license.

from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from apis.versions import views
from common.apis.urls import versions

urlpatterns = [
    re_path(versions.URLS_VERSIONS_INSTALLED, views.VersionsInstalledView.as_view()),
    re_path(
        versions.URLS_VERSIONS_COMPATIBILITY,
        views.VersionsCompatibilityView.as_view(),
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
