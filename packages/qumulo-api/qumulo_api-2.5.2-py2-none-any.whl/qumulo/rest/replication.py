# Copyright (c) 2016 Qumulo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import qumulo.lib.request as request
from qumulo.lib.uri import UriBuilder

@request.request
def start_listener(conninfo, credentials, target_dir):
    body = {'target_dir': target_dir}
    method = "POST"
    uri = UriBuilder(path="/v1/replication/start-listener")
    return request.rest_request(
        conninfo, credentials, method, unicode(uri), body=body)

@request.request
def stop_listener(conninfo, credentials):
    method = "POST"
    uri = UriBuilder(path="/v1/replication/stop-listener")
    return request.rest_request(conninfo, credentials, method, unicode(uri))

@request.request
def replicate_file(conninfo, credentials, filename, address, port):
    body = {'filename': filename, 'address': address, 'port': port}
    method = "POST"
    uri = UriBuilder(path="/v1/replication/replicate-file")
    return request.rest_request(
        conninfo, credentials, method, unicode(uri), body=body)
