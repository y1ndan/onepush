"""
@Project   : onepush
@Author    : y1ndan
@Blog      : https://www.yindan.me
"""

from ..core import Provider


class Custom(Provider):
    name = 'custom'

    _params = {
        'required': ['url'],
        'optional': ['method', 'datatype', 'data', 'headers']
    }

    def __init__(self):
        super().__init__()
        self.headers = None

    def _prepare_url(self, url: str, **kwargs):
        self.url = url
        return self.url

    def _prepare_data(self,
                      method: str = 'post',
                      datatype: str = 'data',
                      data: dict = None,
                      headers: dict = None,
                      **kwargs):
        self.method = method
        self.datatype = datatype
        self.data = data
        self.headers = headers
        return self.data

    def _send_message(self):
        return super()._send_message(self.headers)
