from tests.test_notifiers.test_webhook_notification import TestWebHookNotification
from vents.notifiers.hipchat_webhook import HipChatWebHookNotifier
from vents.providers.kinds import ProviderKind
from vents.settings import VENTS_CONFIG


class TestHipChatWebHookNotifier(TestWebHookNotification):
    webhook = HipChatWebHookNotifier

    def test_attrs(self):
        assert self.webhook.notification_key == ProviderKind.HIPCHAT
        assert self.webhook.name == "HipChat WebHook"

    def test_prepare(self):
        with self.assertRaises(VENTS_CONFIG.exception):
            self.webhook._prepare(None)
        with self.assertRaises(VENTS_CONFIG.exception):
            self.webhook._prepare({})

        context = {"message": "message"}
        assert self.webhook._prepare(context) == {
            "message": context.get("message"),
            "message_format": context.get("message_format", "html"),
            "color": context.get("color"),
            "from": VENTS_CONFIG.project_name,
            "attach_to": context.get("attach_to"),
            "notify": context.get("notify", False),
            "card": context.get("card"),
        }


del TestWebHookNotification
