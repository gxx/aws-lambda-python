# coding=utf-8
"""ImageResize Lambda function handler"""
from __future__ import print_function

import boto3
from wand.image import Image

from resize import resize_image


def handle_resize(event, context):
    """Handle an S3 event on the target bucket to resize and save to destination bucket

    Example Event:
    {
      "Records": [
        {
          "eventVersion": "2.0",
          "eventTime": "1970-01-01T00:00:00.000Z",
          "requestParameters": {
            "sourceIPAddress": "127.0.0.1"
          },
          "s3": {
            "configurationId": "testConfigRule",
            "object": {
              "eTag": "0123456789abcdef0123456789abcdef",
              "sequencer": "0A1B2C3D4E5F678901",
              "key": "HappyFace.jpg",
              "size": 1024
            },
            "bucket": {
              "arn": "arn:aws:s3:::mybucket",
              "name": "sourcebucket",
              "ownerIdentity": {
                "principalId": "EXAMPLE"
              }
            },
            "s3SchemaVersion": "1.0"
          },
          "responseElements": {
            "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH",
            "x-amz-request-id": "EXAMPLE123456789"
          },
          "awsRegion": "us-east-1",
          "eventName": "ObjectCreated:Put",
          "userIdentity": {
            "principalId": "EXAMPLE"
          },
          "eventSource": "aws:s3"
        }
      ]
    }

    :param event: Information of the event which triggered the invocation of this function
    :type event: dict
    :param context: The invocation context
    :type context: dict
    """
    # Obtain the bucket name and key for the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key_path = event['Records'][0]['s3']['object']['key']

    # Retrieve the S3 Object
    s3_connection = boto3.resource('s3')
    s3_object = s3_connection.Object(bucket_name, key_path)

    response = s3_object.get()

    # Perform the resize operation
    with Image(blob=response['Body'].read()) as image:
        resized_image = resize_image(image, 400, 400)
        resized_data = resized_image.make_blob()

    # And finally, upload to the resize bucket the new image
    s3_resized_object = s3_connection.Object('test-resize', key_path)
    s3_resized_object.put(ACL='authenticated-read', Body=resized_data)

    # Finally remove, as the bucket is public and we don't want just anyone dumping the list of our files!
    s3_object.delete()


