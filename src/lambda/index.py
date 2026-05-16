import os
import boto3
import urllib.parse

s3 = boto3.client('s3', endpoint_url=os.environ.get('AWS_ENDPOINT_URL'))
sns = boto3.client('sns', endpoint_url=os.environ.get('AWS_ENDPOINT_URL'))

def handler(event, context):
    try:
        sns_topic_arn = os.environ.get('SNS_TOPIC_ARN')
        for record in event['Records']:
            src_bucket = record['s3']['bucket']['name']
            src_key = urllib.parse.unquote_plus(record['s3']['object']['key'])
            
            print(f"Copy file {src_key} from bucket {src_bucket}...")
            
            s3.copy_object(
                Bucket='s3-finish',
                Key=src_key,
                CopySource={'Bucket': src_bucket, 'Key': src_key}
            )
            print("File copied!")
            
            if sns_topic_arn:
                sns.publish(
                    TopicArn=sns_topic_arn,
                    Message=f"File {src_key} automaticly moved s3-finish.",
                    Subject="S3 Automation Notification"
                )
    except Exception as e:
        print(f"Error: {e}")
        raise e
    return {"status": "ok"}