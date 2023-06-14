#!/usr/bin/env python
import boto3
import os
import logging
import time

from flask import Flask

logging.basicConfig(level=logging.INFO)
application = Flask(__name__)

FILE_NAME = 'test.zip'
s3_bucket_name_template = 'panicks-test-beta'

session = boto3.Session()
s3client = session.client(service_name='s3', region_name=os.environ.get("AWS_REGION"))
stsClient = boto3.client('sts')
identity_response = stsClient.get_caller_identity()

caller_account_id = identity_response['Account']
s3_bucket_name = s3_bucket_name_template.format(caller_account_id)
logging.info("Retrieving data from s3 bucket {}".format(s3_bucket_name))

loop_start = time.time()
while(time.time() - loop_start < 90):
  start_time = time.time()
  response = s3client.get_object(
    Bucket=s3_bucket_name,
    Key=FILE_NAME
  )

  time_taken = time.time() - start_time
  logging.info("Finished downloading file from s3 in {} seconds".format(time_taken))
  time.sleep(3)
  logging.info(response)

if __name__ == '__main__':
    port = int(os.environ.get("FLASK_RUN_PORT", 8000))
    application.run(host='0.0.0.0', debug=False, port=port)
