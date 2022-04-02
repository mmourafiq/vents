#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
# This file and its contents are licensed under the AGPLv3 License.
# Please see the included NOTICE for copyright information and
# LICENSE-AGPL for a copy of the license.

from common.query.service import QueryService
from common.service_interface import LazyServiceWrapper

backend = LazyServiceWrapper(
    backend_base=QueryService,
    backend_path="common.query.service.QueryService",
    options={},
)
backend.expose(locals())
