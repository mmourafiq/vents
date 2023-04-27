from typing import Dict

from vents.notifiers.spec import NotificationSpec
from vents.notifiers.webhook import WebHookNotifier
from vents.providers.kinds import ProviderKind
from vents.settings import VENTS_CONFIG


class DiscordWebHookNotifier(WebHookNotifier):
    notification_key = ProviderKind.DISCORD
    name = "Discord WebHook"
    description = "Discord webhooks to send payload to a discord room."
    raise_empty_context = True

    @classmethod
    def serialize_notification_to_context(cls, notification: NotificationSpec) -> Dict:
        return {"content": notification.details}

    @classmethod
    def _prepare(cls, context: Dict) -> Dict:
        context = super()._prepare(context)

        payload = {
            "username": VENTS_CONFIG.project_name,
            "avatar_url": context.get("avatar_url") or VENTS_CONFIG.project_icon,
            "tts": context.get("tts", False),
        }
        content = context.get("content")
        if content and len(content) <= 2000:
            payload["content"] = content
        else:
            raise VENTS_CONFIG.exception(
                "Discord content must non null and 2000 or fewer characters."
            )

        proxy = context.get("proxy")
        if proxy:
            payload["https"] = proxy
        return payload
