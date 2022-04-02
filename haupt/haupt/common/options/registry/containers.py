#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
# This file and its contents are licensed under the AGPLv3 License.
# Please see the included NOTICE for copyright information and
# LICENSE-AGPL for a copy of the license.

from common.options import option_namespaces, option_subjects
from common.options.option import Option, OptionScope, OptionStores
from polyaxon import types
from polyaxon.auxiliaries import (
    V1PolyaxonInitContainer,
    V1PolyaxonSidecarContainer,
    get_default_init_container,
    get_default_sidecar_container,
)

INIT_CONTAINER = "{}_{}".format(option_namespaces.INIT, option_subjects.CONTAINER)

SIDECAR_CONTAINER = "{}_{}".format(
    option_namespaces.SIDECARS, option_subjects.CONTAINER
)

OPTIONS = {SIDECAR_CONTAINER, INIT_CONTAINER}


class PolyaxonInitContainer(Option):
    key = INIT_CONTAINER
    description = "The docker image to use for init container"
    scope = OptionScope.GLOBAL
    is_secret = False
    is_optional = True
    is_list = False
    typing = types.STR
    store = OptionStores.SETTINGS
    options = None

    @staticmethod
    def get_default_value():
        return get_default_init_container(schema=False)

    @classmethod
    def _extra_processing(cls, value):
        if not value:
            return value
        V1PolyaxonInitContainer.from_dict(value)
        return value


class PolyaxonSidecarContainer(Option):
    key = SIDECAR_CONTAINER
    description = "Sidecar container definition"
    scope = OptionScope.GLOBAL
    is_secret = False
    is_optional = True
    is_list = False
    typing = types.DICT
    store = OptionStores.SETTINGS
    options = None

    @staticmethod
    def get_default_value():
        return get_default_sidecar_container(schema=False)

    @classmethod
    def _extra_processing(cls, value):
        if not value:
            return value
        V1PolyaxonSidecarContainer.from_dict(value)
        return value
