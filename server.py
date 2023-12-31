#!/usr/bin/env python
import hashlib

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
def heath():
  return "<p>Successfully downloaded file from S3</p>"

@application.route("/test")
def hello_world():
  request_start = time.time()

  FILE_NAME = 'download'

  session = boto3.Session()
  s3client = session.client(service_name='s3', region_name=os.environ.get("AWS_REGION"))
  logging.info("Downloading file {}".format(FILE_NAME))

  s3_bucket_name = 'test-bucket-xx'

  randnum = random.randint(1, 1000)
  loop_time = 1000
  if randnum <= 800:
    loop_time = 200
  elif randnum <= 950:
    loop_time = 500

  loop_start = time.time()
  response_list = []
  while((time.time() - loop_start) * 1000 < loop_time):
    start_time = time.time()
    response = s3client.get_object(
      Bucket=s3_bucket_name,
      Key=FILE_NAME
    )
    time_taken = (time.time() - start_time)*1000
    logging.info("[{}] Download Duration {} ms.".format(time.ctime(), time_taken))


    data = response['Body'].read()
    for count in range(2):
      h = hashlib.sha3_256(data)
      response_list.append(h)

    time_taken = (time.time() - start_time)*1000
    logging.info("[{}] Process Duration {} ms.".format(time.ctime(), time_taken))


  request_time = (time.time() - request_start)*1000;
  logging.info("[{}] E2E Request Time {}. Loop time {}".format(time.ctime(), request_time, loop_time))

  logging.info(response_list.__sizeof__())
  return "<p>Successfully downloaded file from S3</p>"

if __name__ == '__main__':
    port = int(os.environ.get("FLASK_RUN_PORT", 80))
    application.run(host='0.0.0.0', debug=False, port=port, threaded=True)