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
  s3_bucket_name_template = 'slow-launch-bucket'
  
  session = boto3.Session()
  s3client = session.client(service_name='s3', region_name=os.environ.get("AWS_REGION"))
  stsClient = boto3.client('sts')
  identity_response = stsClient.get_caller_identity()
  loop_start = time.time()
  logging.info("Downloading file {}".format(loop_start))
  
  caller_account_id = identity_response['Account']
  s3_bucket_name = s3_bucket_name_template.format(caller_account_id)
  
  while(time.time() - loop_start < 90):
    start_time = time.time()
    response = s3client.get_object(
      Bucket=s3_bucket_name,
      Key=FILE_NAME
    )
    
    time_taken = (time.time() - start_time)*1000;
    if (time.time() - loop_start >= 60):
      logging.info("[{}] Throttled Dowload Duration {} ms".format(time.time(), time_taken ))
    else:
      logging.info("[{}] Dowload Duration {} ms".format(time.time(), time_taken ))
    time.sleep(3)
    
  return "<p>Hello, World!</p>"

if __name__ == '__main__':
    #hello_world()
    port = int(os.environ.get("FLASK_RUN_PORT", 8000))
    application.run(host='0.0.0.0', debug=False, port=port)
