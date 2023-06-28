#!/usr/bin/env python
import boto3
import os
import logging
import time

from flask import Flask

logging.basicConfig(level=logging.INFO)
application = Flask(__name__)

@application.route("/")
def hello_world():
  logging.info("Downloading file")
  FILE_NAME = 'download'
  
  session = boto3.Session()
  s3client = session.client(service_name='s3', region_name=os.environ.get("AWS_REGION"))
  stsClient = boto3.client('sts')
  identity_response = stsClient.get_caller_identity()
  logging.info("Downloading file {}".format(loop_start))
  
  caller_account_id = identity_response['Account']
  s3_bucket_name = 'test-bucket-071049406198'

  start_time = time.time()
  response = s3client.get_object(
    Bucket=s3_bucket_name,
    Key=FILE_NAME
  )  
  time_taken = (time.time() - start_time)*1000;
  logging.info("[{}] Download Duration {} ms".format(time.time(), time_taken ))

  return "<p>Successfully downloaded file from S3</p>"

if __name__ == '__main__':
    port = int(os.environ.get("FLASK_RUN_PORT", 8000))
    application.run(host='0.0.0.0', debug=False, port=port)
