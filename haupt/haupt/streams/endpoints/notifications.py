#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
# This file and its contents are licensed under the AGPLv3 License.
# Please see the included NOTICE for copyright information and
# LICENSE-AGPL for a copy of the license.
import logging

import ujson

from rest_framework import status

from django.core.handlers.asgi import ASGIRequest
from django.db import transaction
from django.http import HttpResponse
from django.urls import path

from polyaxon import settings
from polyaxon.lifecycle import V1StatusCondition
from streams.endpoints.base import UJSONResponse
from streams.tasks.notification import notify_run

logger = logging.getLogger("haupt.streams.notifications")


@transaction.non_atomic_requests
async def notify(
    request: ASGIRequest, namespace: str, owner: str, project: str, run_uuid: str
) -> HttpResponse:
    body = ujson.loads(request.body)
    run_name = body.get("name")
    condition = body.get("condition")
    if not condition:
        errors = "Received a notification request without condition."
        logger.warning(errors)
        return UJSONResponse(
            data={"errors": errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
    condition = V1StatusCondition.get_condition(**condition)
    connections = body.get("connections")
    if not connections:
        errors = "Received a notification request without connections."
        logger.warning(errors)
        return UJSONResponse(
            data={"errors": errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not settings.AGENT_CONFIG.connections:
        errors = "Received a notification request, but the agent did not declare connections."
        logger.warning(errors)
        return UJSONResponse(
            data={"errors": errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    await notify_run(
        namespace=namespace,
        owner=owner,
        project=project,
        run_uuid=run_uuid,
        run_name=run_name,
        condition=condition,
        connections=connections,
    )
    return HttpResponse(status=status.HTTP_200_OK)


URLS_RUNS_NOTIFY = (
    "<str:namespace>/<str:owner>/<str:project>/runs/<str:run_uuid>/notify"
)

# fmt: off
notifications_routes = [
    path(
        URLS_RUNS_NOTIFY,
        notify,
        # name="notify",
        # methods=["POST"],
    ),
]
