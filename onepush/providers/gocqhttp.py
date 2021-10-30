"""
@Project   : onepush
@Author    : y1ndan
@Blog      : https://www.yindan.me
"""

from ..core import Provider


class Gocqhttp(Provider):
    name = 'gocqhttp'
    base_url = 'http://{}:{}/send_private_msg'

    _params = {
        'required': ['ip_domain', 'port', 'qq'],
        'optional': ['title', 'content']
    }

    def _prepare_url(self, ip_domain: str = '127.0.0.1', port: int = 5700, **kwargs):
        self.url = self.base_url.format(ip_domain, port)
        return self.url

    def _prepare_data(self,
                      qq: int,
                      title: str = None,
                      content: str = None,
                      **kwargs):
        message = self.process_message(title, content)
        self.data = {'user_id':qq, 'message': message}
        return self.data
      
