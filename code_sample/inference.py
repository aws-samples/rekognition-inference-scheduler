import json
import boto3
client=boto3.client('rekognition')

#Replace the below value with the project version ARN
model = "arn:aws:rekognition:us-east-1:123456789012:project/logos_2/version/logos_2.2022-12-08T23.28.31/1670522312291"

def lambda_handler(event, context):
    
    print(event)
    s3_details = json.loads(event["Records"][0]["body"])["Records"][0]["s3"]
    
    bucket_name = s3_details["bucket"]["name"]
    print(bucket_name)
    
    object_key = s3_details["object"]["key"]
    print(object_key)
    

    #Call DetectCustomLabels
    response = client.detect_custom_labels(Image={'S3Object': {'Bucket': bucket_name, 'Name': object_key}},
        MinConfidence=0,
        ProjectVersionArn=model)
    
    print(response)

    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
