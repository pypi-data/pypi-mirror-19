# (C) Copyright 2014, 2015 Hewlett Packard Enterprise Development Company LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from monascaclient.apiclient import base

from six.moves.urllib import parse
from six.moves.urllib_parse import unquote


class MonascaManager(base.BaseManager):

    def __init__(self, client, **kwargs):
        super(MonascaManager, self).__init__(client)

    def _parse_body(self, body):
        if type(body) is dict:
            self.next = None
            for link in body['links']:
                if link['rel'] == 'next':
                    self.next = link['href']
            return body['elements']
        else:
            return body

    def _list(self, path, dim_key=None, **kwargs):
        """Get a list of metrics."""
        url_str = self.base_url + path
        newheaders = self.get_headers()
        if dim_key and dim_key in kwargs:
            dimstr = self.get_dimensions_url_string(kwargs[dim_key])
            kwargs[dim_key] = dimstr

        if kwargs:
            url_str += '?%s' % parse.urlencode(kwargs, True)
        resp, body = self.client.json_request(
            'GET', url_str, headers=newheaders)
        return self._parse_body(body)

    def get_headers(self):
        headers = self.client.credentials_headers()
        return headers

    def get_dimensions_url_string(self, dimdict):
        dim_list = list()
        for k, v in dimdict.items():
            # In case user specifies a dimension multiple times
            if isinstance(v, (list, tuple)):
                v = v[-1]
            if v:
                dim_str = k + ':' + v
            else:
                dim_str = k
            dim_list.append(dim_str)
        return ','.join(dim_list)

    def list_next(self):
        if hasattr(self, 'next') and self.next:
            self.next = unquote(self.next)
            path = self.next.split(self.base_url, 1)[-1]
            return self._list(path)
        return None
