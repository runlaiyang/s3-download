#!/usr/bin/env python
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
  logging.info("Downloading file")

  session = boto3.Session()
  s3client = session.client(service_name='s3', region_name=os.environ.get("AWS_REGION"))
  stsClient = boto3.client('sts')
  identity_response = stsClient.get_caller_identity()
  caller_account_id = identity_response['Account']
  s3_bucket_name = 'test-bucket-071049406198'

  200ms_file = '200'
  500ms_file = '500'
  1000ms_file = '1000'

  randnum = random.randint(1, 1000)

  FILE_NAME = 1000ms_file
  if randnum <= 800:
    FILE_NAME = 200ms_file
  elif randnum <= 950:
    FILE_NAME = 500ms_file

  logging.info("Downloading file {}".format(FILE_NAME))
  start_time = time.time()
  response = s3client.get_object(
    Bucket=s3_bucket_name,
    Key=FILE_NAME
  )  
  time_taken = (time.time() - start_time)*1000;
  logging.info("[{}] Download Duration {} ms".format(time.ctime(), time_taken ))

  return "<p>Successfully downloaded file from S3</p>"

if __name__ == '__main__':
    port = int(os.environ.get("FLASK_RUN_PORT", 8000))
    application.run(host='0.0.0.0', debug=False, port=port, threaded=True)