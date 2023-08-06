from slackclient import SlackClient
class SlackEngine(object):
    def __init__(self, config):
        '''
            Params:
                - config (dict):
                    - SLACK_TOKEN: your authentication token from Slack
        '''
        # set slack token
        self.token = config.get('SLACK_TOKEN', None)
        if not self.token:
            raise ValueError("Please add a SLACK_TOKEN to your config file.")
        self.slack_client = SlackClient(self.token)

    def find_channels(self):
        channels_call = self.slack_client.api_call("channels.info")
        if not channels_call['ok']:
            return channels_call['ok']
        return None

    def channel_info(self,channel_id):
        channel_info = slack_client.api_call("channels.info", channel=channel_id)
        if channel_info:
            return channel_info['channel']
        return None

    def send_message(self,channel_id,message):
        self.slack_client.api_call(
            "chat.postMessage",
            channel=channel_id,
            text=message,
            username='velbot',
            mrkdwn="true",
            icon_emoji=':robot_face:'
        )

    def send_attachment(channel_id, attachment,text=''):
        self.slack_client.api_call(
            "chat.postMessage",
            channel=channel_id,
            attachments=attachment,
            text=text,
            username='velbot',
            icon_emoji=':robot_face:'
        )
