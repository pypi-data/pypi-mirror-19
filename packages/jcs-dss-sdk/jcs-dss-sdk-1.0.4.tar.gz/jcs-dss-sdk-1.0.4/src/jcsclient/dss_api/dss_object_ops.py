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
import math
import hmac
import json
import base64
import requests
import exceptions
from email.utils import formatdate
import xml.sax
import json
import xmltodict
from jcsclient.filechunkio import *

class ObjectOp(DSSOp):

    def __init__(self):
        DSSOp.__init__(self)

    def parse_args(self, options=None):
        params = {}
        self.dss_op_path = '/' + self.bucket_name + '/' + self.object_name


    def validate_args(self):
        pass

    def execute(self):
        resp = self.make_request()
        return resp

    def process_result(self, result):
        if result is not None:
            status = result.status_code
            if status != 200 and status != 204:
                response_json = {"headers": result.headers, "status_code": result.status_code,
                                 "status_message": result.reason, "error_message": result.text}
            else:
                response_json = {"headers": result.headers, "status_code": result.status_code,
                                 "status_message": result.reason}
        else:
            response_json = {"status_code": "500", "error_message": "Connection not established"}
        return response_json


class DeleteObjectOp(ObjectOp):

    def __init__(self, buckname, objname):
        ObjectOp.__init__(self)
        self.http_method = 'DELETE'
        self.bucket_name = buckname
        self.object_name = objname


class HeadObjectOp(ObjectOp):

    def __init__(self, buckname, objname):
        ObjectOp.__init__(self)
        self.http_method = 'HEAD'
        self.object_name = objname
        self.bucket_name = buckname


class MultipartUpload(object):
    def __init__(self, bucketName, objectName, input_file_path, chunkSize=5 * 1024 * 1024 * 1024):
        self.bucketName = bucketName
        self.objectName = objectName
        self.chunkSize = chunkSize
        self.file_path = input_file_path

    def initiate(self):
        print("\nInitiating multipart upload")
        op = InitMPUploadOp(self.bucketName, self.objectName)
        op.parse_args()
        resp = op.execute()
        op.raise_for_failure(resp)
        self.uploadId = xmltodict.parse(resp.content)["InitiateMultipartUploadResult"]["UploadId"]
        self.numParts = 0
        self.parts = []
        op.process_result(resp)

    def cancel(self):
        pass

    def listParts(self):
        pass

    def partsToXML(self):
        s = '<CompleteMultipartUpload>\n'
        for (partNum, partEtag) in self.parts:
            s += '  <Part>\n'
            s += '    <PartNumber>%d</PartNumber>\n' % partNum
            s += '    <ETag>%s</ETag>\n' % partEtag
            s += '  </Part>\n'
        s += '</CompleteMultipartUpload>'
        return s

    def uploadPart(self, partNum, fp, size):
        print("\nUploading part number " + str(partNum))
        dict = {"upload_id": self.uploadId, "part_number": str(partNum), "file_path": self.file_path}
        op = UploadPartOp(self.bucketName, self.objectName)
        op.parse_args(dict)
        resp = op.execute(fp, size)
        op.raise_for_failure(resp)
        partEtag = resp.headers["etag"]
        self.numParts += 1
        self.parts.append((partNum, partEtag))

    def complete(self):
        print("\nCompleting multipart upload")
        op = CompleteMPUploadOp(self.bucketName, self.objectName)
        dict = {"upload_id": self.uploadId, "mp_parts_file": ""}
        op.parse_args(dict)
        xmlStr = self.partsToXML()
        resp = op.execute(xmlStr)
        return resp


class PutObjectOp(ObjectOp):

    def __init__(self, bucketname, objname, path, enc):
        ObjectOp.__init__(self)
        self.http_method = 'PUT'
        self.object_name =objname
        self.bucket_name = bucketname
        self.local_file_name = path
        self.encryption= enc

    def execute(self):
        # get signature
        processResult = self.put_single_object(self.object_name, self.local_file_name)
        return processResult

    def put_single_object(self, object_name, input_file_path, is_folder=False):
        statinfo = os.stat(input_file_path)
        if (not is_folder and statinfo.st_size > 5 * 1024 * 1024 * 1024):
            return self.put_single_object_multipart(object_name, input_file_path)

        self.dss_op_path = '/' + self.bucket_name + '/' + object_name
        self.dss_op_path = urllib2.quote(self.dss_op_path.encode("utf8"))
        # get signature
        date_str = formatdate(usegmt=True)
        auth = DSSAuth(self.http_method, self.access_key, self.secret_key, date_str, self.dss_op_path,
                       content_type='application/octet-stream', use_encryption=self.encryption)
        signature = auth.get_signature()
        self.http_headers['Authorization'] = signature
        self.http_headers['Date'] = date_str
        if (self.encryption):
            self.http_headers['x-jcs-server-side-encryption'] = 'AES256'
        if (is_folder):
            self.http_headers['Content-Length'] = 0
        else:
            self.http_headers['Content-Length'] = str(statinfo.st_size)
        self.http_headers['Content-Type'] = 'application/octet-stream'

        # construct request
        request_url = self.dss_url + self.dss_op_path
        data = None
        if (not is_folder):
            data = open(input_file_path, 'rb')
        # make request
        resp = requests.put(request_url, headers=self.http_headers, data=data, verify=self.is_secure_request)
        return resp

    def put_single_object_multipart(self, object_name, input_file_path):
        part_size = 5 * 1024 * 1024 * 1024
        statinfo = os.stat(input_file_path)
        total_size = statinfo.st_size
        print("\nPerforming multipart upload as the size of file " + input_file_path + " is greater that 5GB : " + str(
            total_size))
        part_count = int(math.ceil(total_size / float(part_size)))
        mp = MultipartUpload(self.bucket_name, object_name, input_file_path)
        mp.initiate()
        for i in range(part_count):
            offset = part_size * i
            bytes = min(part_size, total_size - offset)
            with FileChunkIO(input_file_path, 'r', offset=offset, bytes=bytes) as fp:
                mp.uploadPart(i + 1, fp, bytes)
        return mp.complete()



class GetObjectOp(ObjectOp):


    def __init__(self, buckname, objname, outpath=None):
        ObjectOp.__init__(self)
        self.http_method = 'GET'
        self.bucket_name = buckname
        self.object_name = objname
        self.local_file_name = outpath

    def parse_args(self, options):
        if(self.local_file_name is None):
            self.local_file_name = self.object_name
        self.dss_op_path = '/' + self.bucket_name + '/' + self.object_name
        self.dss_op_path = urllib2.quote(self.dss_op_path.encode("utf8"))


    def validate_args(self):
        pass

    def execute(self):
        # get signature
        date_str = formatdate(usegmt=True)
        auth = DSSAuth(self.http_method, self.access_key, self.secret_key, date_str, self.dss_op_path)
        signature = auth.get_signature()
        self.http_headers['Authorization'] = signature
        self.http_headers['Date'] = formatdate(usegmt=True)

        # construct request
        request_url = self.dss_url + self.dss_op_path
        # make request
        resp = ''
        with open(self.local_file_name, 'wb') as handle:
            resp = requests.get(request_url, headers = self.http_headers, stream = True, verify = self.is_secure_request)
            if resp.ok:
                for block in resp.iter_content(10240):
                    handle.write(block)
            else:
                resp.raise_for_status()

        return resp


class InitMPUploadOp(ObjectOp):


    def __init__(self, buckname, objname):
        ObjectOp.__init__(self)
        self.http_method = 'POST'
        self.dss_query_str = 'uploads'
        self.dss_query_str_for_signature = 'uploads'
        self.bucket_name = buckname
        self.object_name = objname

    def process_result(self, result):
        if result.status_code == 200:
            xmldict = xmltodict.parse(result.content)
            resdict = {"headers": result.headers, "status_code": result.status_code, "status_message": result.reason, "UploadId": xmldict['InitiateMultipartUploadResult']['UploadId']}

        else:
            xmldict = xmltodict.parse(result.content)
            resdict = {"headers": result.headers, "status_code": result.status_code, "status_message": result.reason, "error_message": xmldict['Error']['Message'], "error_message": xmldict['Error']['Code']}
        return resdict


class CancelMPUploadOp(ObjectOp):

    def __init__(self, buckname, objname, uploadId):
        ObjectOp.__init__(self)
        self.http_method = 'DELETE'
        self.bucket_name = buckname
        self.object_name = objname
        self.upload_id = uploadId

    def parse_args(self, args_dict):
        self.dss_op_path = '/' + self.bucket_name + '/' + self.object_name
        self.dss_op_path = urllib2.quote(self.dss_op_path.encode("utf8"))
        self.dss_query_str = 'uploadId=' + self.upload_id
        self.dss_query_str_for_signature = 'uploadId=' + self.upload_id


class ListPartsOp(ObjectOp):

    def __init__(self, buckname, objname, upload_id, outfile):
        ObjectOp.__init__(self)
        self.http_method = 'GET'
        self.object_name = objname
        self.bucket_name = buckname
        self.upload_id = upload_id
        self.outfile = outfile

    def parse_args(self, args_dict):
        params = {}
        self.dss_op_path = '/' + self.bucket_name + '/' + self.object_name
        self.dss_op_path = urllib2.quote(self.dss_op_path.encode("utf8"))
        self.dss_query_str = 'uploadId=' + self.upload_id + "&max-parts=2048"
        self.dss_query_str_for_signature = 'uploadId=' + self.upload_id


    def execute(self):
        resp = self.make_request()
        if (self.outfile is not None):
            self.raise_for_failure(resp)
            parts = xmltodict.parse(resp.content)["ListPartsResult"]["Part"]
            s = '<CompleteMultipartUpload>\n'
            for part in parts:
                s += '  <Part>\n'
                s += '    <PartNumber>%s</PartNumber>\n' % part["PartNumber"]
                s += '    <ETag>%s</ETag>\n' % part["ETag"]
                s += '  </Part>\n'
            s += '</CompleteMultipartUpload>'
            fp = open(self.outfile, "w")
            fp.write(s)
            fp.close()
        return resp

    def process_result(self, result, outfile):
        # nonop currently
        if result.status_code == 200:
            if outfile is not None:
                resdict = {"headers": result.headers, "status_code": result.status_code, "status_message": result.reason}
            else:
                resdict = {"headers": result.headers, "status_code": result.status_code, "status_message": result.reason, "content": result.content}
        else:
            resdict = {"headers": result.headers, "status_code": result.status_code, "status_message": result.reason, "error_message": result.text}
        return resdict

class UploadPartOp(ObjectOp):

    def __init__(self, buckname, objname):
        ObjectOp.__init__(self)
        self.http_method = 'PUT'
        self.bucket_name = buckname
        self.object_name = objname

    def parse_args(self, args_dict):
        self.upload_id = args_dict['upload_id']
        self.part_number = args_dict['part_number']
        self.local_file_name = args_dict['file_path']
        self.dss_op_path = '/' + self.bucket_name + '/' + self.object_name
        self.dss_query_str = 'partNumber=' + self.part_number + '&uploadId=' + self.upload_id
        self.dss_query_str_for_signature = 'partNumber=' + self.part_number + '&uploadId=' + self.upload_id


    def execute(self, fp=None, size=None):
        # get signature
        date_str = formatdate(usegmt=True)
        query_str = 'partNumber=' + self.part_number + '&uploadId=' + self.upload_id
        auth = DSSAuth(self.http_method, self.access_key, self.secret_key, date_str, self.dss_op_path,
                       query_str=self.dss_query_str_for_signature, content_type='application/octet-stream')
        signature = auth.get_signature()
        self.http_headers['Authorization'] = signature
        self.http_headers['Date'] = date_str
        if (fp is None and size is None):
            statinfo = os.stat(self.local_file_name)
            self.http_headers['Content-Length'] = str(statinfo.st_size)
        else:
            self.http_headers['Content-Length'] = str(size)

        self.http_headers['Content-Type'] = 'application/octet-stream'

        # construct request
        request_url = self.dss_url + self.dss_op_path
        if (self.dss_query_str is not None):
            request_url += '?' + self.dss_query_str
        if (fp is None):
            data = open(self.local_file_name, 'rb')
        else:
            data = fp
        # make request
        resp = None
        if (fp is None and size is None):
            resp = requests.put(request_url, headers=self.http_headers, data=data, verify=self.is_secure_request)
        else:
            s = requests.Session()
            req = requests.Request('PUT', request_url, headers=self.http_headers, data=data)
            prepped = req.prepare()
            prepped.headers['Content-Length'] = str(size)
            resp = s.send(prepped, verify=self.is_secure_request)
        return resp


class CompleteMPUploadOp(ObjectOp):

    def __init__(self, buckname, objname):
        ObjectOp.__init__(self)
        self.http_method = 'POST'
        self.bucket_name = buckname
        self.object_name = objname

    def parse_args(self, args_dict):
        params = {}
        self.upload_id = args_dict['upload_id']
        self.local_file_name = args_dict['mp_parts_file']
        self.dss_op_path = '/' + self.bucket_name + '/' + self.object_name
        self.dss_op_path = urllib2.quote(self.dss_op_path.encode("utf8"))
        self.dss_query_str = 'uploadId=' + self.upload_id
        self.dss_query_str_for_signature = 'uploadId=' + self.upload_id


    def execute(self, xmlStr=None):
        # get signature
        date_str = formatdate(usegmt=True)
        auth = DSSAuth(self.http_method, self.access_key, self.secret_key, date_str, self.dss_op_path,
                       query_str=self.dss_query_str_for_signature, content_type='text/xml')
        signature = auth.get_signature()
        self.http_headers['Authorization'] = signature
        self.http_headers['Date'] = date_str
        if (xmlStr is None):
            statinfo = os.stat(self.local_file_name)
            self.http_headers['Content-Length'] = str(statinfo.st_size)
        else:
            self.http_headers['Content-Length'] = str(len(xmlStr))
        self.http_headers['Content-Type'] = 'text/xml'

        # construct request
        request_url = self.dss_url + self.dss_op_path
        if (self.dss_query_str is not None):
            request_url += '?' + self.dss_query_str
        if (xmlStr is None):
            data = open(self.local_file_name, 'rb')
        else:
            data = xmlStr
        # make request
        resp = requests.post(request_url, headers=self.http_headers, data=data, verify=self.is_secure_request)

        # process response
        return resp


class RenameObjectOp(ObjectOp):
    def __init__(self, buckname, objname, newName):
        ObjectOp.__init__(self)
        self.http_method = 'PUT'
        self.bucket_name = buckname
        self.object_name = objname
        self.new_name = newName

    def parse_args(self, args_dict):
        pass

    def execute(self):
        self.dss_op_path = '/' + self.bucket_name + '/' + self.object_name
        self.dss_op_path = urllib2.quote(self.dss_op_path.encode("utf8"))
        # get signature
        date_str = formatdate(usegmt=True)
        auth = DSSAuth(self.http_method, self.access_key, self.secret_key, date_str, self.dss_op_path,
                       content_type='application/octet-stream')
        signature = auth.get_signature()
        self.http_headers['Authorization'] = signature
        self.http_headers['Date'] = date_str
        self.http_headers['Content-Type'] = 'application/octet-stream'

        # construct request
        query_params = "?newname=" + urllib2.quote(self.new_name.encode("utf8"))
        request_url = self.dss_url + urllib2.quote(self.dss_op_path.encode("utf8")) + query_params
        # make request
        resp = requests.put(request_url, headers=self.http_headers, data=None, verify=self.is_secure_request)
        return resp


class GetPresignedURLOp(ObjectOp):
    def __init__(self, buckname, objname, expiry):
        ObjectOp.__init__(self)
        self.http_method = 'GET'
        self.bucket_name = buckname
        self.object_name = objname
        self.validity = expiry

    def parse_args(self, args_dict):
        params = {}
        self.dss_op_path = '/' + self.bucket_name + '/' + self.object_name
        self.dss_op_path = urllib2.quote(self.dss_op_path.encode("utf8"))

    def validate_args(self):
        pass

    def execute(self):
        # get signature
        date_str = formatdate(usegmt=True)
        expiry_time = int(time.time()) + int(self.validity)
        auth = DSSAuth(self.http_method, self.access_key, self.secret_key, date_str, self.dss_op_path,
                       use_time_in_seconds=True, expiry_time=expiry_time)
        signature = auth.get_signature()
        # url encode the signature

        # construct url
        request_url = self.dss_url + self.dss_op_path
        request_url = request_url + '?JCSAccessKeyId=' + self.access_key + '&Expires=' + str(
            expiry_time) + '&Signature=' + urllib2.quote(signature.encode("utf8"))
        response_json = '{"DownloadUrl": "' + request_url + '"}'
        return response_json

    def process_result(self, result):
        # nonop currently, just dump a json in case of success
        return result


class CopyObjectOp(ObjectOp):
    def __init__(self, buckname, objname, copysource):
        ObjectOp.__init__(self)
        self.http_method = 'PUT'
        self.bucket_name = buckname
        self.object_name = objname
        self.copy_source = copysource

    def parse_args(self, args):
        params = {}
        self.dss_op_path = '/' + self.bucket_name + '/' + self.object_name
        self.dss_op_path = urllib2.quote(self.dss_op_path.encode("utf8"))

    def validate_args(self):
        # check for valid copy source should be <bucket>/<object>
        pos = self.copy_source.find('/')
        if (pos == -1 or pos == 0 or pos == len(self.copy_source) - 1):
            raise ValueError('copy-source should be of format <bucket-name>/<object-name>')

    def execute(self):
        self.http_headers['x-jcs-metadata-directive'] = 'COPY'
        self.http_headers['x-jcs-copy-source'] = self.copy_source

        resp = self.make_request()
        return resp

