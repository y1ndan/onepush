"""
@Project   : onepush
@Author    : y1ndan
@Blog      : https://www.yindan.me
"""

from ..core import Provider
from ..exceptions import NotificationError


class WPush(Provider):
    name = 'wpush'
    base_url = 'https://api.wpush.cn/api/v1/send'
    site_url = 'https://wpush.cn/docs'

    _params = {
        'required': ['apikey', 'content'],
        'optional': ['title', 'channel', 'topic_code']
    }

    def _prepare_url(self, **kwargs):
        self.url = self.base_url
        return self.url

    def _prepare_data(self,
                      content: str,
                      apikey: str = None,
                      title: str = None,
                      channel: str = None,
                      topic_code: str = None,
                      **kwargs):
        self.data = {
            'apikey': apikey,
            'title': title if title else content,
            'content': content,
            'channel': channel or 'wechat',
        }
        if topic_code:
            self.data['topic_code'] = topic_code
        return self.data

    def _send_message(self):
        # Credential POST: do not follow redirects; never log apikey.
        response = self.request(
            'post',
            self.url,
            self.proxies,
            json=self.data,
            allow_redirects=False,
        )
        if response is None:
            raise NotificationError('WPUSH request failed: no response')
        try:
            result = response.json()
        except Exception as e:
            raise NotificationError(
                'WPUSH request failed: invalid JSON response'
            ) from e
        # Success ONLY when JSON code is the integer 0
        # (reject missing / null / bool; bool is an int subclass).
        code = result.get('code')
        if type(code) is not int or code != 0:
            message = result.get('message') or result
            raise NotificationError(
                'WPUSH request failed: {}'.format(message)
            )
        return response
