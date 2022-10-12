#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
# This file and its contents are licensed under the AGPLv3 License.
# Please see the included NOTICE for copyright information and
# LICENSE-AGPL for a copy of the license.

from haupt.proxies.generators.base import write_to_conf_file
from haupt.proxies.schemas.api import get_base_config, get_main_config


def generate_api_conf(path=None, root=None):
    write_to_conf_file("polyaxon.main", get_main_config(root), path)
    write_to_conf_file("polyaxon.base", get_base_config(), path)
