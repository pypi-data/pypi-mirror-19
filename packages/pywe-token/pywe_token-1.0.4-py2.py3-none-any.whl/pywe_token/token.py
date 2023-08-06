# -*- coding: utf-8 -*-

import time

from pywe_base import BaseWechat
from pywe_exception import WeChatException
from pywe_storage import MemoryStorage


class Token(BaseWechat):
    def __init__(self, appid=None, secret=None, storage=None):
        # 获取access token, Refer: https://mp.weixin.qq.com/wiki/14/9f9c82c1af308e3b14ba9b973f99a8ba.html
        super(Token, self).__init__()
        self.WECHAT_ACCESS_TOKEN = self.API_DOMAIN + '/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}'
        self.appid = appid
        self.secret = secret
        self.storage = storage or MemoryStorage()
        self.token = None
        self.expires_at = None

    @property
    def access_info_key(self):
        return '{}:access:info'.format(self.appid)

    def __about_to_expires(self, expires_at):
        return expires_at and expires_at - int(time.time()) < 60

    def __fetch_access_token(self, appid=None, secret=None, storage=None):
        access_info = self.get(self.WECHAT_ACCESS_TOKEN, appid=appid or self.appid, secret=secret or self.secret)
        if 'expires_in' not in access_info:
            raise WeChatException(access_info)
        self.token = access_info.get('access_token')
        expires_in = access_info.get('expires_in')
        self.expires_at = int(time.time()) + expires_in
        storage = storage or self.storage
        if storage:
            access_info['expires_at'] = self.expires_at
            storage.set(self.access_info_key, access_info, expires_in)
        return self.token

    def access_token(self, appid=None, secret=None, storage=None):
        if self.token and not self.__about_to_expires(self.expires_at):
            return self.token
        # Init appid/secret/storage
        self.appid = appid or self.appid
        self.secret = secret or self.secret
        self.storage = storage or self.storage
        # Fetch access_info
        access_info = self.storage.get(self.access_info_key)
        if access_info:
            access_token = access_info.get('access_token')
            if access_token and not self.__about_to_expires(access_info.get('expires_at')):
                return access_token
        return self.__fetch_access_token(appid, secret, storage)


token = Token()
access_token = token.access_token
