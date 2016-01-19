# coding=utf-8
"""ImageList Lambda function handler"""
from __future__ import print_function

import os

import boto3
from jinja2 import Environment
from jinja2 import FileSystemLoader


def _render_template(image_urls):
    env = Environment(loader=FileSystemLoader(os.path.abspath(os.path.dirname(__file__))))
    template = env.get_template('list.html')
    rendered_template = template.render(image_urls=image_urls)
    return rendered_template


def handle_list_image(event, context):
    """Handle a listImage function call and return JSON containing HTML code as the property 'htmlContent'

    :param event: Information of the event which triggered the invocation of this function
    :type event: dict
    :param context: The invocation context
    :type context: dict
    """
    s3_connection = boto3.resource('s3')
    bucket = s3_connection.Bucket('test-resized')

    image_summaries = [image_summary for image_summary in bucket.objects.all()]
    image_summaries.sort(key=lambda o: o.last_modified)

    print('Found {} image summaries'.format(len(image_summaries)))

    s3_client = boto3.client('s3')

    image_urls = []
    for summary in image_summaries:
        image_urls.append(
            s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': summary.bucket_name,
                    'Key': summary.key
                }
            )
        )

    return {'htmlContent': _render_template(image_urls)}


