#!/usr/bin/env python

import matplotlib.pyplot as plt
import boto3 
import random
from datetime import datetime

numOfArgs = int(input("How many points are being plotted?\n"))
title = input("What is the title of this graph?\n")

x = []
y = []
i=1

while i < numOfArgs + 1:
    x.append(int(input("X {}:\n".format(i))))
    y.append(int(input("Y {}:\n".format(i))))
    i += 1

timestamp = datetime.utcnow().strftime('%B %d %Y - %H:%M')

plt.plot(x, y)
plt.title(title)
rannum = random.randint(1000, 99999999999999)
filename = "graphs/{}.png".format(rannum)
plt.savefig(filename)



s3 = boto3.client('s3')
bucket = '<your bucket name>'
extra_args={'ACL': 'public-read'}
s3.upload_file(filename, bucket, filename, extra_args)
s3link = 'https://s3-eu-west-1.amazonaws.com/<your_bucket_name>/{}'.format(filename)


ses = boto3.client('ses')
response = ses.send_email(
    Destination={
        'ToAddresses': [
            '<your_whitelisted_email_address>'
        ],
    },
    Message={
        'Body': {
            'Html': {
                'Charset': 'UTF-8',
                'Data': 'Click <a class="ulink" href="{}" target="_blank">Here </a>to see your generated graph.'.format(s3link),
            },
            'Text': {
                'Charset': 'UTF-8',
                'Data': 'Click on this link to view your generated graph: {}'.format(s3link),
            },
        },
        'Subject': {
            'Charset': 'UTF-8',
            'Data': 'New Graph {}'.format(timestamp),
        },
    },
    Source='<your_whitelisted_from_email>'
)

exit()