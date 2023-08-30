import json
import boto3

rekognition_client = boto3.client('rekognition')
lambda_client = boto3.client('lambda')


def lambda_handler(event, context):

    #Replace ProjectVersionArn paramter with the relevant value
    response = rekognition_client.stop_project_version(
    ProjectVersionArn='arn:aws:rekognition:us-east-1:333997476486:project/logos_2/version/logos_2.2022-12-08T23.28.31/1670522312291')
    
    print(response)

    #Replace UUID and FunctionName paramters with the relevant values
    response = lambda_client.update_event_source_mapping(
    UUID='8921ca0f-beb3-40d0-ad20-d4ae29a2e6f6',
    FunctionName='inference-function',
    Enabled=False,
    BatchSize=1)
    
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
