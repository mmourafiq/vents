from tests.test_notifiers.test_webhook_notification import TestWebHookNotification
from vents.notifiers.mattermost_webhook import MattermostWebHookNotifier
from vents.providers.kinds import ProviderKind
from vents.settings import VENTS_CONFIG


class TestMattermostWebHookNotifier(TestWebHookNotification):
    webhook = MattermostWebHookNotifier

    def test_attrs(self):
        assert self.webhook.notification_key == ProviderKind.MATTERMOST
        assert self.webhook.name == "Mattermost WebHook"

    def test_validate_config(self):
        assert self.webhook._validate_config(
            {
                "url": "http://mattermost.com/webhook/foo",
                "method": "post",
                "channel": "foo",
            }
        ) == [
            {
                "url": "http://mattermost.com/webhook/foo",
                "method": "POST",
                "channel": "foo",
            }
        ]

        assert self.webhook._validate_config(
            [
                {
                    "url": "http://mattermost.com/webhook/foo",
                    "method": "post",
                    "channel": "foo",
                },
                {"url": "http://mattermost.com/webhook/bar", "method": "GET"},
            ]
        ) == [
            {
                "url": "http://mattermost.com/webhook/foo",
                "method": "POST",
                "channel": "foo",
            },
            {"url": "http://mattermost.com/webhook/bar", "method": "GET"},
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
                    "pretext": context.get("pretext"),
                    "title": context.get("title"),
                    "text": context.get("text"),
                    "color": context.get("color"),
                    "fields": None,
                    "author_name": VENTS_CONFIG.project_name,
                    "author_link": VENTS_CONFIG.project_url,
                    "author_icon": VENTS_CONFIG.project_icon,
                }
            ]
        }


del TestWebHookNotification
