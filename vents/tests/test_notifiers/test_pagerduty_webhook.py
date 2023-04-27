from tests.test_notifiers.test_webhook_notification import TestWebHookNotification
from vents.notifiers.pagerduty_webhook import PagerDutyWebHookNotifier
from vents.providers.kinds import ProviderKind
from vents.settings import VENTS_CONFIG


class TestPagerDutyWebHook(TestWebHookNotification):
    webhook = PagerDutyWebHookNotifier

    def test_attrs(self):
        assert self.webhook.notification_key == ProviderKind.PAGERDUTY
        assert self.webhook.name == "PagerDuty WebHook"

    def test_validate_config(self):
        assert self.webhook._validate_config(
            {
                "url": "http://pagerduty.com/webhook/foo",
                "method": "post",
                "service_key": "foo",
            }
        ) == [
            {
                "url": "http://pagerduty.com/webhook/foo",
                "method": "POST",
                "service_key": "foo",
            }
        ]

        assert self.webhook._validate_config(
            [
                {
                    "url": "http://pagerduty.com/webhook/foo",
                    "method": "post",
                    "service_key": "foo",
                },
                {"url": "http://pagerduty.com/webhook/bar", "method": "GET"},
            ]
        ) == [
            {
                "url": "http://pagerduty.com/webhook/foo",
                "method": "POST",
                "service_key": "foo",
            },
            {"url": "http://pagerduty.com/webhook/bar", "method": "GET"},
        ]

    def test_get_config(self):
        assert self.webhook.get_config(
            {"url": "http://foo.com/webhook", "method": "post", "service_key": "foo"}
        ) == [{"url": "http://foo.com/webhook", "method": "POST", "service_key": "foo"}]
        assert self.webhook.get_config(
            [
                {
                    "url": "http://foo.com/webhook",
                    "method": "post",
                    "service_key": "foo",
                },
                {
                    "url": "http://bar.com/webhook",
                    "method": "GET",
                    "service_key": "bar",
                },
            ]
        ) == [
            {"url": "http://foo.com/webhook", "method": "POST", "service_key": "foo"},
            {"url": "http://bar.com/webhook", "method": "GET", "service_key": "bar"},
        ]

    def test_prepare(self):
        with self.assertRaises(VENTS_CONFIG.exception):
            self.webhook._prepare(None)
        with self.assertRaises(VENTS_CONFIG.exception):
            self.webhook._prepare({})

        context = {"title": "title", "text": "text"}
        assert self.webhook._prepare(context) == {
            "event_type": context.get("event_type"),
            "description": context.get("description"),
            "details": context.get("details"),
            "incident_key": context.get("incident_key"),
            "client": VENTS_CONFIG.project_name,
            "client_url": VENTS_CONFIG.project_url,
            "contexts": context.get("contexts"),
        }


del TestWebHookNotification
