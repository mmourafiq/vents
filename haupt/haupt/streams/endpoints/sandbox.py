#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
# This file and its contents are licensed under the AGPLv3 License.
# Please see the included NOTICE for copyright information and
# LICENSE-AGPL for a copy of the license.
import os

from rest_framework import status

from django.core.handlers.asgi import ASGIRequest
from django.http import HttpResponse
from django.urls import path

from polyaxon import settings
from polyaxon.api import API_V1_LOCATION
from polyaxon.contexts import paths as ctx_paths
from polyaxon.lifecycle import V1ProjectFeature
from streams.endpoints.base import ConfigResponse, UJSONResponse


async def get_run_details(request: ASGIRequest, run_uuid: str) -> HttpResponse:
    subpath = os.path.join(run_uuid, ctx_paths.CONTEXT_LOCAL_RUN)
    data_path = settings.SANDBOX_CONFIG.get_store_path(
        subpath=subpath, entity=V1ProjectFeature.RUNTIME
    )
    if not os.path.exists(data_path) or not os.path.isfile(data_path):
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    with open(data_path, "r") as config_file:
        config_str = config_file.read()
    return ConfigResponse(config_str)


async def get_run_artifact_lineage(request: ASGIRequest, run_uuid: str) -> HttpResponse:
    subpath = os.path.join(run_uuid, ctx_paths.CONTEXT_LOCAL_LINEAGES)
    data_path = settings.SANDBOX_CONFIG.get_store_path(
        subpath=subpath, entity=V1ProjectFeature.RUNTIME
    )
    if not os.path.exists(data_path) or not os.path.isfile(data_path):
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    with open(data_path, "r") as config_file:
        config_str = config_file.read()
        config_str = f'{{"results": {config_str}}}'

    return ConfigResponse(config_str)


async def list_runs(request: ASGIRequest) -> HttpResponse:
    # project = request.path_params["project"]
    data_path = settings.SANDBOX_CONFIG.get_store_path(
        subpath="", entity=V1ProjectFeature.RUNTIME
    )
    if not os.path.exists(data_path) or not os.path.isdir(data_path):
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    data = []
    for run in os.listdir(data_path):
        run_path = os.path.join(data_path, run, ctx_paths.CONTEXT_LOCAL_RUN)
        if not os.path.exists(run_path) or not os.path.isfile(run_path):
            continue

        with open(run_path, "r") as config_file:
            data.append(config_file.read())
    data_str = ",".join(data)
    config_str = f'{{"results": [{data_str}], "count": {len(data)}}}'
    return ConfigResponse(config_str)


async def get_project_details(request: ASGIRequest, project: str) -> HttpResponse:
    data_path = settings.SANDBOX_CONFIG.get_store_path(
        subpath=project, entity="project"
    )
    if not os.path.exists(data_path) or not os.path.isdir(data_path):
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    data_path = os.path.join(data_path, ctx_paths.CONTEXT_LOCAL_PROJECT)
    if os.path.exists(data_path) and os.path.isfile(data_path):
        with open(data_path, "r") as config_file:
            config_str = config_file.read()
        return ConfigResponse(config_str)

    # Use basic project configuration
    return UJSONResponse({"name": project})


async def list_projects(request: ASGIRequest) -> HttpResponse:
    data_path = settings.SANDBOX_CONFIG.get_store_path(subpath="", entity="project")
    if not os.path.exists(data_path) or not os.path.isdir(data_path):
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    data = []
    for proj in os.listdir(data_path):

        data_path = os.path.join(data_path, proj, ctx_paths.CONTEXT_LOCAL_PROJECT)
        if os.path.exists(data_path) and os.path.isfile(data_path):
            with open(data_path, "r") as config_file:
                data.append(config_file.read())
        else:
            data.append(f'{{"name": "{proj}"}}')

    data_str = ",".join(data)
    config_str = f'{{"results": [{data_str}], "count": {len(data)}}}'
    return ConfigResponse(config_str)


URLS_RUNS_DETAILS = API_V1_LOCATION + "<str:owner>/<str:project>/runs/<str:run_uuid>/"
URLS_RUNS_STATUSES = (
    API_V1_LOCATION + "<str:owner>/<str:project>/runs/<str:run_uuid>/statuses"
)
URLS_RUNS_LINEAGE_ARTIFACTS = (
    API_V1_LOCATION + "<str:owner>/<str:project>/runs/<str:run_uuid>/lineage/artifacts"
)
URLS_RUNS_LIST = API_V1_LOCATION + "<str:owner>/<str:project>/runs/"
URLS_PROJECTS_LIST = API_V1_LOCATION + "<str:owner>/projects/list"
URLS_PROJECTS_DETAILS = API_V1_LOCATION + "<str:owner>/<str:project>/"

# fmt: off
sandbox_routes = [
    path(
        URLS_RUNS_DETAILS,
        get_run_details,
        # name="get_run_details",
        # methods=["GET"],
    ),
    path(
        URLS_RUNS_STATUSES,
        get_run_details,
        # name="get_run_details",
        # methods=["GET"],
    ),
    path(
        URLS_RUNS_LINEAGE_ARTIFACTS,
        get_run_artifact_lineage,
        # name="get_run_artifact_lineage",
        # methods=["GET"],
    ),
    path(
        URLS_RUNS_LIST,
        list_runs,
        # name="list_runs",
        # methods=["GET"],
    ),
    path(
        URLS_PROJECTS_LIST,
        list_projects,
        # name="get_project_details",
        # methods=["GET"],
    ),
    path(
        URLS_PROJECTS_DETAILS,
        get_project_details,
        # name="get_project_details",
        # methods=["GET"],
    ),
]
