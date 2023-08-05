import boto3
import json
import urllib
import botocore

def update_job(key, value):
    try:
        client_lambda = boto3.client('lambda', region_name='us-east-1')

        # get instance id from aws
        url = "http://169.254.169.254/latest/meta-data/instance-id"
        instance_id = urllib.urlopen(url).read()

        json_params = {
            'instance_id': instance_id,
            key: value
        }

        client_lambda.invoke(
            FunctionName='had-rds-update',
            InvocationType='Event',
            Payload=json.dumps(json_params)
        )
    except botocore.exceptions.NoCredentialsError as e:
        print "NoCredentialsError: {}. Most likely running outside of HAD API Service environment".format(e)
        return

    except botocore.exceptions.ClientError as e:
        print "ClientError: {}".format(e)
        raise
