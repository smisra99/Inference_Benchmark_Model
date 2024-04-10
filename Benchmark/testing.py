from PIL import Image
from io import BytesIO
import boto3

import os
os.environ["AWS_DEFAULT_REGION"] = 'us-east-1'
os.environ["AWS_ACCESS_KEY_ID"] = 'AKIA52QUT77PDFHDKUXW'
os.environ["AWS_SECRET_ACCESS_KEY"] = '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'

BUCKET = 'image-for-benchmark'
FOLDER = 'images/'

s3 = boto3.client('s3')
paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=BUCKET, Prefix=FOLDER)

for page in pages:
    for obj in page['Contents']:
        x=(obj["Key"])
        print(x)


file_byte_string = s3.get_object(Bucket=BUCKET, Key=x)['Body'].read()
x=Image.open(BytesIO(file_byte_string))
x.show()