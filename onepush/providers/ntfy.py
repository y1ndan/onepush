import base64

from ..core import Provider


class Ntfy(Provider):
    name = 'ntfy'
    _params = {
        'required': ['url', 'content', 'topic'],
        'optional': ['token', 'title', 'tags', 'priority', 'actions', 'click', 'attach', 'markdown', 'icon', 'filename', 'delay', 'email', 'call', 'username', 'password']
    }

    def _prepare_url(self, url: str, **kwargs):
        self.url = url
        return self.url

    def _prepare_data(self, topic: str,
                      content: str,
                      title: str = None,
                      priority: int = 0,
                      token: str = None,
                      ** kwargs):
        if kwargs.get('username') and kwargs.get('password'):
            token = "Basic " + base64.b64encode(
                (kwargs.get('username') + ':' + kwargs.get('password')).encode('utf-8')).decode('utf-8')
        elif token:
            token = "Bearer " + token
        else:
            token = None
        self.data = {
            'topic': topic,
            'title': title,
            'message': content,
            'priority': priority,
            'token': token
        }
        return self.data

    def _send_message(self):
        data = self.data.copy()
        token = self.data.get('token')
        headers = {'Authorization': token} if token else None
        data.pop('token', None)
        return self.request('post', self.url, json=data, headers=headers)
