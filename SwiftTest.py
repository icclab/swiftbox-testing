# -*- coding: utf-8 -*-

'''
Copyright 2014 ZHAW (Zürcher Hochschule für Angewandte Wissenschaften)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

__author__ = 'gank'

from swiftclient.client import Connection
from swiftclient.client import get_object
from swiftclient.client import put_object
from Configuration import Configuration


class SwiftObjectManager(object):
    def __init__(self, storage_url, token):
        super(SwiftObjectManager,self).__init__()
        self._storage_url = storage_url
        self._token = token

    def upload(self):
        put_object(self._storage_url, self._token, Configuration.container_name, Configuration.object_name,
                   Configuration.object_content)

    def download(self):
        with open(Configuration.down_file_name,'w') as f:
            f.write(get_object(self._storage_url, self._token, Configuration.container_name, Configuration.object_name)[1])


class SwiftAuthManager(object):
    def __init__(self):
        super(SwiftAuthManager, self).__init__()
        self._cnt = self._auth()

    def _auth(self):
        cnt = Connection(authurl=Configuration.auth_url, user=Configuration.username, key=Configuration.password,
                         tenant_name=Configuration.tenant_name, auth_version=2, insecure=False)
        return cnt

    def getcredentials(self):
        storage_url, token = self._cnt.get_auth()
        return storage_url, token


def main():
    sam = SwiftAuthManager()
    storage_url, token = sam.getcredentials()

    som = SwiftObjectManager(storage_url, token)
    som.upload()
    som.download()
    with open(Configuration.down_file_name) as f:
         assert(Configuration.object_content == f.read())

if __name__ == '__main__':
    main()

