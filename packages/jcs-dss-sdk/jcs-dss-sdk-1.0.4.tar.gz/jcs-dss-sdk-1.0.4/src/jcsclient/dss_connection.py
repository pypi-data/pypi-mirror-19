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

from jcsclient.dss_api.dss_bucket_ops import *
from jcsclient.dss_api.dss_object_ops import *
from jcsclient.config import *


class DSSConnection(object):
    """DSS main class, each cli command is processed here
    Object is created from inside the dss Controller
    """

    def __init__(self, url, access_key, secret_key, secure, debug):
        setup_config_handler(url, access_key, secret_key, secure, debug)

    def operate(self, op, options=None):
        op.parse_args(options)
        op.validate_args()
        result = op.execute()
        processed_result = op.process_result(result)
        return processed_result

    def main(self):
        pass

    def create_bucket(self, bucketName):
        op = CreateBucketOp(bucketName)
        result = self.operate(op)
        return result

    def delete_bucket(self, bucketName):
        op = DeleteBucketOp(bucketName)
        result = self.operate(op)
        return result

    def head_bucket(self, bucketName):
        op = HeadBucketOp(bucketName)
        result = self.operate(op)
        return result

    def list_buckets(self):
        op = ListBucketsOp()
        result = self.operate(op)
        return result

    def delete_object(self, buckName, objName):
        op = DeleteObjectOp(buckName, objName)
        result = self.operate(op, options=None)
        return result

    def get_object(self, buckName, objName, path=None):
        op = GetObjectOp(buckName, objName, path)
        result = self.operate(op, options=None)
        return result

    def list_objects(self, buckName, options=None):
        op = ListObjectsOp(buckName)
        result = self.operate(op, options)
        return result

    def head_object(self, buckName, objName):
        op = HeadObjectOp(buckName, objName)
        result = self.operate(op, options=None)
        return result

    def put_object(self, buckName, objName, path, encryption=False):
        op = PutObjectOp(buckName, objName, path, encryption)
        result = self.operate(op)
        return result

    def init_multipart_upload(self, bucketname, keyname):
        op = InitMPUploadOp(bucketname, keyname)
        result = self.operate(op)
        return result

    def upload_multipart_parts(self, buckname, keyname, args_dict, data_path, size):
        op = UploadPartOp(buckname=buckname, objname=keyname)
        op.parse_args(args_dict)
        res = op.execute(fp=data_path, size=size)
        result = op.process_result(res)
        return result

    def complete_multipart_upload(self, bucketname, keyname, args_dict):
        op = CompleteMPUploadOp(bucketname, keyname)
        result = self.operate(op, args_dict)
        return result

    def cancel_multipart_upload(self, bucketname, keyname, uploadId):
        op = CancelMPUploadOp(bucketname, keyname, uploadId)
        result = self.operate(op, options=None)
        return result

    def list_multipart_parts(self, bucketname, keyname, upload_id, outfile=None):
        op = ListPartsOp(bucketname, keyname, upload_id, outfile)
        op.parse_args(args_dict=None)
        op.validate_args()
        result = op.execute()
        processed_result = op.process_result(result, outfile)
        return processed_result

    def list_multipart_uploads(self, buckname):
        op = ListMPUploadsOp(buckname)
        result = self.operate(op)
        return result

    def copy_object(self, buckname, keyname, sourceName):
        op = CopyObjectOp(buckname=buckname, objname=keyname, copysource=sourceName)
        result = self.operate(op, options=None)
        return result

    def get_presigned_url(self, buckname, objname, expiry):
        op = GetPresignedURLOp(buckname=buckname, objname=objname, expiry=expiry)
        result = self.operate(op, options=None)
        return result

    def rename_object(self, buckname, objname, newName):
        op = RenameObjectOp(buckname=buckname, objname=objname, newName=newName)
        result = self.operate(op, options=None)
        return result
