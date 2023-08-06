# -*- coding=utf-8

from __future__ import absolute_import
# from coscmd.signaturer import Signature
from coscmd.auth import CosS3Auth
from urllib import quote
import time
import requests
from lxml import etree
from os import path
from hashlib import sha1
from contextlib import closing


class CosConfig(object):
    def __init__(self, appid, region, bucket, access_id, access_key):
        self._appid = appid
        self._region = region
        self._bucket = bucket
        self._access_id = access_id
        self._access_key = access_key

    def uri(self, path=None):
        if path:
            return "http://{bucket}-{uid}.{region}.myqcloud.com/{path}".format(
                bucket=self._bucket,
                uid=self._appid,
                region=self._region,
                path=quote(path)
            )
        else:
            return "http://{bucket}-{uid}.{region}.myqcloud.com".format(
                bucket=self._bucket,
                uid=self._appid,
                region=self._region
            )


class MultiPartUpload(object):

    def __init__(self, filename, object_name, conf):
        self._filename = filename
        self._object_name = object_name
        self._conf = conf
        self._upload_id = None
	self._sha1 = []

    def init_mp(self):
        url = self._conf.uri(path=self._object_name)
        print url
        rt = requests.post(url=url+"?uploads", auth=CosS3Auth(self._conf._access_id, self._conf._access_key))
        print rt.status_code, rt.headers, rt.text
	root = etree.XML(rt.text)
	self._upload_id = root.getchildren()[2].text
        return rt.status_code == 200

    def upload_parts(self):
        
      file_size = path.getsize(self._filename)
      # 50 parts, max chunk size 5 MB
      # chunk_size = 10 * 1024 * 1024 # 10 MB
      chunk_size = 1024 * 1024
      while file_size / chunk_size > 10000:
	chunk_size = chunk_size * 10 

      parts_size = (file_size + chunk_size - 1) / chunk_size  
      print "chunk_size: ", chunk_size
      print "parts_size: ", (file_size + chunk_size - 1)/chunk_size
      
      with open(self._filename, 'r') as f:     
	# /ObjectName?partNumber=PartNumber&uploadId=UploadId
	for i in range(parts_size):
	  data = f.read(chunk_size)
	  sha1_etag = sha1()
	  sha1_etag.update(data)
	  self._sha1.append(sha1_etag.hexdigest())
          url = self._conf.uri(path=self._object_name)+"?partNumber={partnum}&uploadId={uploadid}".format(partnum=i+1, uploadid=self._upload_id)
	  print "url: ", url
	  rt = requests.put(url=url,
	                     auth=CosS3Auth(self._conf._access_id, self._conf._access_key),
			     data=data)
	  print "multi part result: ", rt.status_code, rt.headers, rt.text

    def complete_mp(self):
        pass

	root = etree.Element("CompleteMultipartUpload")
	for i, v in enumerate(self._sha1):
	  t = etree.Element("Part")
	  t1 = etree.Element("PartNumber")
	  t1.text = str(i+1)

	  t2 = etree.Element("ETag")
	  t2.text = '"{v}"'.format(v=v)

	  t.append(t1)
	  t.append(t2)
	  root.append(t)
	data = etree.tostring(root)
	url = self._conf.uri(path=self._object_name)+"?uploadId={uploadid}".format(uploadid=self._upload_id)
	print 'complete url', url
	print "data: ", data
	with closing(requests.post(url, auth=CosS3Auth(self._conf._access_id, self._conf._access_key), data=data, stream=True)) as rt:
	  print rt.status_code
	  print rt.text
	  print rt.headers
	return rt.status_code == 200

class CosS3Client(object):

    def __init__(self, conf):
        self._conf = conf

    def put_object_from_filename(self, filename, object_name):
        url = self._conf.uri(object_name)

        from os.path import exists
        if exists(filename):
            with open(filename, 'r') as f:
                rt = requests.put(url, data=f.read(), auth=CosS3Auth(self._conf._access_id, self._conf._access_key))
                return rt.status_code == 200
        else:
            raise IOError("{f} doesn't exist".format(f=filename))

    def multipart_upload_from_filename(self, filename, object_name):
        return MultiPartUpload(filename=filename, object_name=object_name, conf=self._conf)


if __name__ == "__main__":

    conf = CosConfig(appid="1252448703",
                     bucket="sdktestgz",
                     region="cn-south",
                     access_id="AKID15IsskiBQKTZbAo6WhgcBqVls9SmuG00",
                     access_key="ciivKvnnrMvSvQpMAWuIz12pThGGlWRW")

    client = CosS3Client(conf)

    # rt = client.put_object_from_filename("auth.py", "auth1.py")
    # print rt

    mp = client.multipart_upload_from_filename("auth.py", "auth2asdf.py")
    print mp.init_mp()
    mp.upload_parts()
    mp.complete_mp()

