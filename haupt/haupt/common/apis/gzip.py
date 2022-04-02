#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
# This file and its contents are licensed under the AGPLv3 License.
# Please see the included NOTICE for copyright information and
# LICENSE-AGPL for a copy of the license.

from functools import wraps

from django.utils.text import compress_string

try:
    import config
except ImportError:
    config = None


class GzipDecorator:
    """Gzip the response and set the respective header."""

    def __call__(self, func):
        @wraps(func)
        def inner(self, request, *args, **kwargs):
            response = func(self, request, *args, **kwargs)

            if (
                config
                and config.is_debug_mode
                and config.is_monolith_service
                and not config.is_testing_env
            ):
                return response

            # Before we can access response.content, the response needs to be rendered.
            response = self.finalize_response(request, response, *args, **kwargs)
            response.render()  # should be rendered, before picklining while storing to cache

            compressed_content = compress_string(response.content)

            # Ensure that the compressed content is actually smaller than the original.
            if len(compressed_content) >= len(response.content):
                return response

            # Replace content with gzipped variant, update respective headers.
            response.content = compressed_content
            response["Content-Length"] = str(len(response.content))
            response["Content-Encoding"] = "gzip"

            return response

        return inner


gzip = GzipDecorator
