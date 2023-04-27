from vents.notifiers.discord_webhook import DiscordWebHookNotifier
from vents.notifiers.hipchat_webhook import HipChatWebHookNotifier
from vents.notifiers.mattermost_webhook import MattermostWebHookNotifier
from vents.notifiers.pagerduty_webhook import PagerDutyWebHookNotifier
from vents.notifiers.slack_webhook import SlackWebHookNotifier
from vents.notifiers.spec import NotificationSpec
from vents.notifiers.webhook import WebHookNotifier

NOTIFIERS = {
    DiscordWebHookNotifier.notification_key: DiscordWebHookNotifier,
    HipChatWebHookNotifier.notification_key: HipChatWebHookNotifier,
    MattermostWebHookNotifier.notification_key: MattermostWebHookNotifier,
    PagerDutyWebHookNotifier.notification_key: PagerDutyWebHookNotifier,
    SlackWebHookNotifier.notification_key: SlackWebHookNotifier,
    WebHookNotifier.notification_key: WebHookNotifier,
}
