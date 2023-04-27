from typing import Dict

from vents.notifiers.spec import NotificationSpec
from vents.notifiers.webhook import WebHookNotifier
from vents.providers.kinds import ProviderKind
from vents.settings import VENTS_CONFIG


class MattermostWebHookNotifier(WebHookNotifier):
    notification_key = ProviderKind.MATTERMOST
    name = "Mattermost WebHook"
    description = "Mattermost webhooks to send payload to a Mattermost channel."
    raise_empty_context = True
    validate_keys = ["channel"]

    @classmethod
    def serialize_notification_to_context(cls, notification: NotificationSpec) -> Dict:
        payload = {
            "title": notification.title,
            "text": notification.details,
            "color": notification.color,
            "fields": [],
            "author_name": VENTS_CONFIG.project_name,
            "author_link": notification.url,
            "author_icon": VENTS_CONFIG.project_icon,
        }

        return payload

    @classmethod
    def _prepare(cls, context):
        context = super()._prepare(context)

        data = {
            "pretext": context.get("pretext"),
            "title": context.get("title"),
            "text": context.get("text"),
            "color": context.get("color"),
            "fields": context.get("fields"),
            "author_name": context.get("author_name", VENTS_CONFIG.project_name),
            "author_link": context.get("author_link", VENTS_CONFIG.project_url),
            "author_icon": context.get("author_icon", VENTS_CONFIG.project_icon),
        }
        return {"attachments": [data]}

    @classmethod
    def _pre_execute_web_hook(cls, data, config):
        channel = config.get("channel")
        if channel:
            data["channel"] = channel

        return data
