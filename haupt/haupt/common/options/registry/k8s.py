#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
# This file and its contents are licensed under the AGPLv3 License.
# Please see the included NOTICE for copyright information and
# LICENSE-AGPL for a copy of the license.

from common.options.option import Option, OptionScope, OptionStores
from polyaxon import types

K8S_NAMESPACE = "K8S_NAMESPACE"
K8S_IN_CLUSTER = "K8S_IN_CLUSTER"

OPTIONS = {K8S_NAMESPACE, K8S_IN_CLUSTER}


class K8SNamespace(Option):
    key = K8S_NAMESPACE
    scope = OptionScope.GLOBAL
    is_secret = False
    is_optional = False
    is_list = False
    typing = types.STR
    store = OptionStores.SETTINGS
    default = None
    options = None


class K8SInCluster(Option):
    key = K8S_IN_CLUSTER
    scope = OptionScope.GLOBAL
    is_secret = False
    is_optional = False
    is_list = False
    typing = types.BOOL
    store = OptionStores.SETTINGS
    default = None
    options = None
