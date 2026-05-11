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
    base_url = 'https://api.day.app/push'
    site_url = 'https://apps.apple.com/us/app/bark-customed-notifications/id1403753865'

    _params = {
        'required': ['device_key'],
        'optional': [
            'title',
            'subtitle',
            'body',
            'markdown',
            'device_keys',
            'level',
            'volume',
            'badge',
            'call',
            'autoCopy',
            'copy',
            'sound',
            'icon',
            'image',
            'group',
            'ciphertext',
            'isArchive',
            'url',
            'action',
            'id',
            'delete',
            'cipherkey',
            'ciphermethod',
            # Custom parameters
            'base_url',
            # Aliases
            'key', # <-> device_key
            'content', # <-> body
            'autocopy', # <-> autoCopy
            'isarchive', # <-> isArchive
        ]
    }

    def _prepare_url(self, base_url: str = None, **kwargs):
        self.method = 'post'

        if base_url:
            self.base_url = base_url

        self.url = self.base_url
        if not self.url.endswith('/push'):
            self.url += '/push'

        return self.url

    def _prepare_data(self,
                      key: str = None,
                      content: str = None,
                      cipherkey: str = None,
                      ciphermethod: str = None,
                      **kwargs):
        self.datatype = 'json'

        params = {
            'title': None,
            'subtitle': None,
            'body': content,
            'markdown': None,
            'device_key': key,
            'device_keys': None,
            'level': None,
            'volume': None,
            'badge': None,
            'call': None,
            'autoCopy': None,
            'copy': None,
            'sound': None,
            'icon': None,
            'image': None,
            'group': None,
            'ciphertext': None,
            'isArchive': None,
            'url': None,
            'action': None,
            'id': None,
            'delete': None,
        }

        for field in params:
            if field in kwargs:
                params[field] = kwargs.get(field)

        if params['autoCopy'] is None and 'autocopy' in kwargs:
            params['autoCopy'] = kwargs.get('autocopy')
        if params['isArchive'] is None and 'isarchive' in kwargs:
            params['isArchive'] = kwargs.get('isarchive')

        # Remove None values to avoid Bark server JSON parsing errors
        self.data = {k: v for k, v in params.items() if v is not None}

        if params['ciphertext']:
            self.data = {
                'ciphertext': params['ciphertext'],
                'device_key': params['device_key'],
                'device_keys': params['device_keys'],
            }
            iv = kwargs.get('iv')
            if iv:
                self.data['iv'] = iv
            self.data = {k: v for k, v in self.data.items() if v is not None}
        else:
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
