#!/usr/bin/env python
from gevent import monkey
monkey.patch_all()

import boto3
import os
import logging
import time
import random

from flask import Flask

logging.basicConfig(level=logging.INFO)
application = Flask(__name__)

@application.route("/")
def hello_world():
  request_start = time.time()

  FILE_NAME = 'download'
  session = boto3.Session()
  s3client = session.client(service_name='s3', region_name=os.environ.get("AWS_REGION"))
  s3_bucket_name = 'test-bucket-071049406198'

  randnum = random.randint(1, 1000)
  loop_time = 1000
  if randnum <= 800:
    loop_time = 200
  elif randnum <= 950:
    loop_time = 500

  loop_start = time.time()
  while((time.time() - loop_start) * 1000 < loop_time):
    start_time = time.time()
    response = s3client.get_object(
      Bucket=s3_bucket_name,
      Key=FILE_NAME
    )  

    time_taken = (time.time() - start_time)*1000;
    logging.info("[{}] Download Duration {} ms.".format(time.ctime(), time_taken))

  request_time = (time.time() - request_start)*1000;
  logging.info("[{}] E2E Request Time {}. Loop time {}".format(time.ctime(), request_time, loop_time))

  return "<p>Successfully downloaded file from S3</p>"

if __name__ == '__main__':
    port = int(os.environ.get("FLASK_RUN_PORT", 8000))
    application.run(host='0.0.0.0', debug=False, port=port, threaded=True)