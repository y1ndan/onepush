"""
@Project   : onepush
@Author    : y1ndan
@Blog      : https://www.yindan.me
"""

import base64
import json
import secrets

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from ..core import Provider


class Bark(Provider):
    name = 'bark'
    base_url = 'https://api.day.app/{}'
    site_url = 'https://apps.apple.com/us/app/bark-customed-notifications/id1403753865'

    _params = {
        'required': ['key'],
        'optional': [
            'title', 'content', 'sound', 'isarchive', 'icon', 'group', 'url', 'copy',
            'autocopy', 'cipherkey', 'ciphermethod',
        ]
    }

    def _prepare_url(self, key: str, **kwargs):
        self.url = key
        if 'https' not in key and 'http' not in key:
            self.url = self.base_url.format(key)
        return self.url

    def _prepare_data(self,
                      title: str = None,
                      content: str = None,
                      sound: str = 'healthnotification',
                      isarchive: int = None,
                      icon: str = None,
                      group: str = None,
                      url: str = None,
                      copy: str = None,
                      autocopy: int = None,
                      cipherkey: str = None,
                      ciphermethod: str = None,
                      **kwargs):
        self.data = {
            'title': title,
            'body': content,
            'sound': sound,
            'isArchive': 1 if isarchive else isarchive,
            'icon': icon,
            'group': group,
            'url': url,
            'copy': copy,
            'autoCopy': 1 if autocopy else autocopy
        }
        self._encrypt_data(cipherkey, ciphermethod)
        return self.data

    def _encrypt_data(self, key: str, method: str):
        if not key or not method:
            return
        if method.lower() == 'cbc':
            self._encrypt_by_cbc(key)
        elif method.lower() == 'ecb':
            self._encrypt_by_ecb(key)

    def _encrypt_by_cbc(self, key: str):
        body = json.dumps(self.data)
        iv = base64.b64encode(secrets.token_bytes(int(AES.block_size / 4 * 3)))
        cipher = AES.new(key.encode(), AES.MODE_CBC, iv=iv)
        cipher_bytes = cipher.encrypt(pad(body.encode(), AES.block_size))
        ciphertext = base64.b64encode(cipher_bytes).decode('ascii')
        self.data = {
            'ciphertext': ciphertext,
            'iv': iv.decode('ascii'),
        }
    
    def _encrypt_by_ecb(self, key: str):
        body = json.dumps(self.data)
        cipher = AES.new(key.encode(), AES.MODE_ECB)
        cipher_bytes = cipher.encrypt(pad(body.encode(), AES.block_size))
        ciphertext = base64.b64encode(cipher_bytes).decode('ascii')
        self.data = {
            'ciphertext': ciphertext,
        }
