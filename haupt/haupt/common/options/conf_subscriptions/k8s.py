#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
# This file and its contents are licensed under the AGPLv3 License.
# Please see the included NOTICE for copyright information and
# LICENSE-AGPL for a copy of the license.

from common import conf
from common.options.registry import k8s

conf.subscribe(k8s.K8SNamespace)
conf.subscribe(k8s.K8SInCluster)
