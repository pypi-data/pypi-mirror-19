# Copyright (c) 2016 Jiocloud.com, Inc. or its affiliates.  All Rights Reserved
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#

from dss_op import *
from dss_auth import *
from jcsclient import utils
import os
import sys
import time
import hmac
import json
import base64
import requests
import exceptions
from email.utils import formatdate
import xml.sax

class BucketOp(DSSOp):

    def __init__(self):
        DSSOp.__init__(self)

    def parse_args(self, options):
      self.dss_op_path = '/' + self.bucket_name

    def validate_args(self):
        pass

    def execute(self):
        resp = self.make_request()
        return resp

    def process_result(self, result, response_json=None):
        if result is not None:
            status = result.status_code
            if status != 200 and status != 204:
                response_json = {"headers": result.headers, "status_code": result.status_code,
                                 "status_message": result.reason, "error_message": result.text}
            else:
                response_json = {"headers": result.headers, "status_code": result.status_code,
                                 "status_message": result.reason, "content": result.content}
        else:
            response_json = {"status_code": "500", "error_message": "Connection not established"}
        return response_json



class ListBucketsOp(BucketOp):

    def __init__(self):
        BucketOp.__init__(self)
        self.dss_op_path = '/'
        self.http_method = 'GET'

    def parse_args(self, options):
        pass

class CreateBucketOp(BucketOp):

    def __init__(self, name):
        BucketOp.__init__(self)
        self.http_method = 'PUT'
        self.bucket_name = name


class DeleteBucketOp(BucketOp):

    def __init__(self, name):
        BucketOp.__init__(self)
        self.bucket_name = name
        self.http_method = 'DELETE'


class HeadBucketOp(BucketOp):

    def __init__(self, name):
        DSSOp.__init__(self)
        self.http_method = 'HEAD'
        self.bucket_name = name


class ListObjectsOp(BucketOp):

    def __init__(self, name):
        DSSOp.__init__(self)
        self.http_method = 'GET'
        self.bucket_name = name

    def parse_args(self, args_dict):
        params = {}
        is_query_params_set = False
        self.dss_query_str = ''

        self.dss_op_path = '/' + self.bucket_name

        if (args_dict is None):
            return

        if(args_dict['prefix'] is not None):
            self.dss_query_str = 'prefix=' + args_dict['prefix']
            is_query_params_set = True

        if(args_dict['marker'] is not None):
            if(not is_query_params_set):
                self.dss_query_str += 'marker=' + args_dict['marker']
                is_query_params_set = True
            else:
                self.dss_query_str += '&marker=' + args_dict['marker']

        if(args_dict['max-keys'] is not None):
            if(not is_query_params_set):
                self.dss_query_str += 'max-keys=' + args_dict['max-keys']
                is_query_params_set = True
            else:
                self.dss_query_str += '&max-keys=' + args_dict['max-keys']

        if(args_dict['delimiter'] is not None):
            if(not is_query_params_set):
                self.dss_query_str += 'delimiter=' + args_dict['delimiter']
                is_query_params_set = True
            else:
                self.dss_query_str += '&delimiter=' + args_dict['delimiter']

        if(self.dss_query_str == ''):
            self.dss_query_str = None


class ListMPUploadsOp(BucketOp):

    def __init__(self, buckname):
        BucketOp.__init__(self)
        self.http_method = 'GET'
        self.dss_query_str_for_signature = 'uploads'
        self.dss_query_str = 'uploads'
        self.bucket_name = buckname

