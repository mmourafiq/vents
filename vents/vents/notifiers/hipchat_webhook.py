from typing import Dict

from vents.notifiers.spec import NotificationSpec
from vents.notifiers.webhook import WebHookNotifier
from vents.providers.kinds import ProviderKind
from vents.settings import VENTS_CONFIG


class HipChatWebHookNotifier(WebHookNotifier):
    notification_key = ProviderKind.HIPCHAT
    name = "HipChat WebHook"
    description = "HipChat webhooks to send payload to a hipchat room."
    raise_empty_context = True

    @classmethod
    def serialize_notification_to_context(cls, notification: NotificationSpec) -> Dict:
        payload = {
            "message": notification.details,
            "message_format": "text",
            "color": notification.color,
            "from": VENTS_CONFIG.project_name,
        }

        return payload

    @classmethod
    def _prepare(cls, context: Dict) -> Dict:
        context = super()._prepare(context)

        return {
            "message": context.get("message"),
            "message_format": context.get("message_format", "html"),
            "color": context.get("color"),
            "from": context.get("from", VENTS_CONFIG.project_name),
            "attach_to": context.get("attach_to"),
            "notify": context.get("notify", False),
            "card": context.get("card"),
        }
