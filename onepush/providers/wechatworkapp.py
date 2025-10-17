"""
@Project   : onepush
@Author    : y1ndan
@Blog      : https://www.yindan.me
"""

from ..core import Provider


class WechatWorkApp(Provider):
    name = 'wechatworkapp'
    base_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'
    site_url = 'https://work.weixin.qq.com/api/doc/90000/90135/90236'

    _params = {
        'required': ['corpid', 'corpsecret', 'agentid'],
        'optional': ['title', 'content', 'touser', 'markdown', 'media_id', 'custom_url']
    }

    def _prepare_url(self, corpid: str, corpsecret: str, **kwargs):
        custom = kwargs.get('custom_url')
        if custom:
            # normalize: if no scheme, assume https
            if not custom.startswith('http://') and not custom.startswith('https://'):
                custom = 'https://' + custom
            # ensure no trailing slash
            custom = custom.rstrip('/')
            url = f"{custom}/cgi-bin/gettoken"
        else:
            url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        data = {'corpid': corpid, 'corpsecret': corpsecret}
        response = self.request('get', url, params=data).json()
        access_token = response.get('access_token')

        # build send message URL; if custom_url present, replace host in base_url
        custom_send = kwargs.get('custom_url')
        if custom_send:
            send_host = custom_send
            if not send_host.startswith('http://') and not send_host.startswith('https://'):
                send_host = 'https://' + send_host
            send_host = send_host.rstrip('/')
            self.url = f"{send_host}/cgi-bin/message/send?access_token={access_token}"
        else:
            self.url = self.base_url.format(access_token)
        return self.url

    def _prepare_data(self,
                      agentid: str,
                      title: str = None,
                      content: str = None,
                      touser: str = '@all',
                      markdown: bool = False,
                      media_id: str = None,
                      **kwargs):
        message = self.process_message(title, content)
        if media_id is None:
            msgtype = 'text'
            if markdown:
                msgtype = 'markdown'

            self.data = {
                'touser': touser,
                'msgtype': msgtype,
                'agentid': agentid,
                msgtype: {
                    'content': message
                }
            }
        else:
            self.data = {
                "touser": touser,
                "msgtype": "mpnews",
                "agentid": agentid,
                "mpnews": {
                    "articles": [
                        {
                            "title": title,
                            "thumb_media_id": media_id,
                            "content_source_url": "",
                            "content": content.replace("\n", "<br/>"),
                            "digest": content,
                        }
                    ]
                },
                "safe": 0
            }
        return self.data

    def _send_message(self):
        return self.request('post', self.url, json=self.data)
