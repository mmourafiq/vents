from typing import Dict

from vents.notifiers.spec import NotificationSpec
from vents.notifiers.webhook import WebHookNotifier
from vents.providers.kinds import ProviderKind
from vents.settings import VENTS_CONFIG


class PagerDutyWebHookNotifier(WebHookNotifier):
    notification_key = ProviderKind.PAGERDUTY
    name = "PagerDuty WebHook"
    description = "PagerDuty webhooks to send event payload to pagerduty."
    raise_empty_context = True
    validate_keys = ["service_key"]

    @classmethod
    def serialize_notification_to_context(cls, notification: NotificationSpec) -> Dict:
        payload = {
            "event_type": notification.title,
            "description": notification.description,
            "details": notification.details,
            "incident_key": "trigger",
            "client": VENTS_CONFIG.project_name,
            "client_url": notification.url,
            "contexts": [],
        }

        return payload

    @classmethod
    def _prepare(cls, context: Dict) -> Dict:
        context = super()._prepare(context)

        return {
            "event_type": context.get("event_type"),
            "description": context.get("description"),
            "details": context.get("details"),
            "incident_key": context.get("incident_key"),
            "client": context.get("client", VENTS_CONFIG.project_name),
            "client_url": context.get("client_url", VENTS_CONFIG.project_url),
            "contexts": context.get("contexts"),
        }

    @classmethod
    def _pre_execute_web_hook(cls, data: Dict, config: Dict) -> Dict:
        service_key = config.get("service_key")
        if service_key:
            data["service_key"] = service_key

        return data
