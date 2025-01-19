from ..core import Provider

class Gotify(Provider):
    name = 'gotify'
    _params = {
        'required': ['url', 'content', 'token'],
        'optional': ['title', 'priority']
    }

    def _prepare_url(self, url: str, token: str, **kwargs):
        self.url = url + '/message?token=' + token
        return self.url

    def _prepare_data(self,
                      content: str,
                      title: str = None,
                      priority: int = 0,
                      **kwargs):
        self.data = {
            'title': title,
            'message': content,
            'priority': priority
        }
        return self.data

    def _send_message(self):
        return self.request('post', self.url, json=self.data)