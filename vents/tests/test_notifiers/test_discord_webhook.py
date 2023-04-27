from unittest.mock import patch

from tests.test_notifiers.test_webhook_notification import TestWebHookNotification
from vents.notifiers.discord_webhook import DiscordWebHookNotifier
from vents.providers.kinds import ProviderKind
from vents.settings import VENTS_CONFIG


class TestDiscordWebHookNotifier(TestWebHookNotification):
    webhook = DiscordWebHookNotifier

    def test_attrs(self):
        assert self.webhook.notification_key == ProviderKind.DISCORD
        assert self.webhook.name == "Discord WebHook"

    def test_prepare(self):
        with self.assertRaises(VENTS_CONFIG.exception):
            self.webhook._prepare(None)
        with self.assertRaises(VENTS_CONFIG.exception):
            self.webhook._prepare({})

        context = {"content": "message"}
        assert self.webhook._prepare(context) == {
            "username": VENTS_CONFIG.project_name,
            "avatar_url": context.get("avatar_url") or VENTS_CONFIG.project_icon,
            "tts": context.get("tts", False),
            "content": "message",
        }

    def test_execute(self):
        with self.assertRaises(VENTS_CONFIG.exception):
            self.webhook.execute(notification=self.notification)

        with patch("vents.notifiers.webhook.safe_request") as mock_execute:
            self.webhook.execute(
                notification=self.notification,
                config={"url": "http://bar.com/webhook", "method": "GET"},
            )

        assert mock_execute.call_count == 1


del TestWebHookNotification
