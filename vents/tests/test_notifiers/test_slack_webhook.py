from tests.test_notifiers.test_webhook_notification import TestWebHookNotification
from vents.notifiers.slack_webhook import SlackWebHookNotifier
from vents.providers.kinds import ProviderKind
from vents.settings import VENTS_CONFIG


class TestSlackWebHookNotifier(TestWebHookNotification):
    webhook = SlackWebHookNotifier

    def test_attrs(self):
        assert self.webhook.notification_key == ProviderKind.SLACK
        assert self.webhook.name == "Slack WebHook"

    def test_validate_config(self):
        assert self.webhook._validate_config(
            {"url": "http://slack.com/webhook/foo", "method": "post", "channel": "foo"}
        ) == [
            {"url": "http://slack.com/webhook/foo", "method": "POST", "channel": "foo"}
        ]

        assert self.webhook._validate_config(
            [
                {
                    "url": "http://slack.com/webhook/foo",
                    "method": "post",
                    "channel": "foo",
                },
                {"url": "http://slack.com/webhook/bar", "method": "GET"},
            ]
        ) == [
            {"url": "http://slack.com/webhook/foo", "method": "POST", "channel": "foo"},
            {"url": "http://slack.com/webhook/bar", "method": "GET"},
        ]

    def test_get_config(self):
        assert self.webhook.get_config(
            {"url": "http://foo.com/webhook", "method": "post", "channel": "foo"}
        ) == [{"url": "http://foo.com/webhook", "method": "POST", "channel": "foo"}]
        assert self.webhook.get_config(
            [
                {"url": "http://foo.com/webhook", "method": "post", "channel": "foo"},
                {"url": "http://bar.com/webhook", "method": "GET", "channel": "bar"},
            ]
        ) == [
            {"url": "http://foo.com/webhook", "method": "POST", "channel": "foo"},
            {"url": "http://bar.com/webhook", "method": "GET", "channel": "bar"},
        ]

    def test_prepare(self):
        with self.assertRaises(VENTS_CONFIG.exception):
            self.webhook._prepare(None)
        with self.assertRaises(VENTS_CONFIG.exception):
            self.webhook._prepare({})

        context = {"title": "title", "text": "text"}
        assert self.webhook._prepare(context) == {
            "attachments": [
                {
                    "fallback": context.get("fallback"),
                    "title": context.get("title"),
                    "title_link": context.get("title_link"),
                    "text": context.get("text"),
                    "fields": context.get("fields"),
                    "mrkdwn_in": None,
                    "footer_icon": context.get("footer_icon"),
                    "footer": context.get("footer", VENTS_CONFIG.project_name),
                    "color": context.get("color"),
                }
            ]
        }


del TestWebHookNotification
