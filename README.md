# Dynamic AWS Rekognition Custom Labels Inference Scheduler with Event-Driven Decoupling 

This solution is designed to address the challenge of optimizing costs associated with Amazon Rekognition Custom Labels inferencing while ensuring data continuity and seamless operation. By leveraging AWS services, we've developed a robust solution that intelligently manages the inferencing endpoint's availability based on business hours.

**Key Features:**
- **Cost Optimization:** Our solution dynamically controls the Amazon Rekognition Custom Labels inference endpoint, ensuring it's active only during business hours. This prevents unnecessary costs incurred from running the endpoint 24/7.

- **Automated Scheduling:** We utilize Amazon EventBridge, a serverless event bus, to create and manage scheduled cron jobs. This allows us to programmatically control the inference endpoint's state according to predefined business requirements.

- **Data Continuity:** To ensure uninterrupted processing of events, we've implemented a decoupling mechanism using Amazon SQS (Simple Queue Service). Events generated during off-business hours are captured and stored as messages in the queue. These messages are processed efficiently when the inference endpoint becomes active again, thus safeguarding data and maintaining smooth operations.


## Overview of Rekognition

Amazon Rekognition is a fully managed AI service provided by AWS. Amazon Rekognition makes it easy to add image and video analysis to your applications.

With Amazon Rekognition Custom Labels, you can identify the objects, logos, and scenes in images that are specific to your business needs. For example, you can find your logo in social media posts, identify your products on store shelves, classify machine parts in an assembly line, distinguish healthy and infected plants, or detect animated characters in images.


## Initial Architecture:

![schdeuler_rekognition drawio](https://github.com/aws-samples/rekognition-inference-scheduler/assets/32926625/3db09ac4-f33d-4cc4-acb6-e8cac30db5ce)

Consider the usecase where the file to be inferenced on are uploaded to an S3 bucket and S3 event notification adds the newly uploaded objects to an SQS Queue. The queue is subscribed by a Lambda Function, that process and get inferencing result from the Rekognition Custom Label.

## Recommended Architecture for scheduling:

![schdeuler_rekognition drawio (1)](https://github.com/aws-samples/rekognition-inference-scheduler/assets/32926625/b90a016a-e7d2-49ff-94ea-683a5b7d8712)

## Workflow

1. EventBridge Scheduler Cronjob triggers the Startup Lambda function at the scheduled time. Ex. 8.30 AM.
2. Startup Lambda function makes the call to start the model using “start_project_version” API.
3. Startup Lambda function enables event source mapping for the source SQS queue and the Inference Lambda function.
4. Once the Rekognition Custom Label Model is live, Inference Lambda can start running inferencing for the uploaded items.
5. EventBridge Scheduler Cronjob will trigger the Shutdown function at the scheduled time (end of the day). Ex. 5.00 PM.
6. Shutdown Lambda Function will remove the event source mapping for the Inference function from the SQS queue.
7. Shutdown Lambda function makes the call to stop the model using “stop_project_version” API.

## Considerations:

1. Implementing the above architecture will stop processing any new items uploaded after the Event Source Mapping is removed by the Shutdown Lambda Function.
2. Starting Rekognition Custom Label Model can take upto 30 minutes. Ensure to schedule the Startup Function trigger well in advance to avoid delay.
3. Items in the queue will not be processed after the Event Source Mapping is removed by the Shutdown Lambda function. These items will be processed after the model is started the next day.

## Step by Step Implementation Guide:
Note: The implementation guide assumes that you already have the following architecture implemented:

![schdeuler_rekognition drawio (2)](https://github.com/aws-samples/rekognition-inference-scheduler/assets/32926625/fdace6ab-caef-4f27-9989-4adfbf3f415d)

To implement scheduling for your Rekognition model, please follow the steps below:

1. ### Create IAM role for Lambda Function:
    1. Search for IAM on the search bar in the management console and select IAM
    2. Click on Roles on the Left sidebar
       ![image (4)](https://github.com/aws-samples/rekognition-inference-scheduler/assets/32926625/4f5a2622-dfdf-4890-9e11-038021e3d7fd)
    3. Click on Create role:
       ![image (5)](https://github.com/aws-samples/rekognition-inference-scheduler/assets/32926625/9d6b50f6-0f7e-47e6-801b-4a57591f399c)
    4. Select Lambda function:
       ![image (6)](https://github.com/aws-samples/rekognition-inference-scheduler/assets/32926625/348a5907-05cf-4b5b-885b-c3c5c55f21e0)
    5. Add Permission for Lambda and Rekognition (LambdaFullAccess and RekognitionFullAccess - ensure to further make the permissions more granular based on the access requriements) . Click Create Role (Note the Name of the Role, will be required in the next step)
        
2. ### Create the Startup Lambda Function:
    1. Search for Lambda on the search bar in the management console and select Lambda from the results.
       ![image (7)](https://github.com/aws-samples/rekognition-inference-scheduler/assets/32926625/7acf168a-5e41-4d5e-baeb-acc9dca90955)
    2. Click on Create Function:
       ![image (8)](https://github.com/aws-samples/rekognition-inference-scheduler/assets/32926625/1861225f-c170-4613-90fc-126ddbad527f)
    3. Add the Function Name and Runtime, click create Function:
       ![image (9)](https://github.com/aws-samples/rekognition-inference-scheduler/assets/32926625/ebfaaf75-481b-4d6c-9f3c-a2c7926abd03)
    4. Import code from startup_function.py (refer code_sample folder in the repository) to the Lambda function. Ensure to replace the following paramters in the code :
        1. Rekognition custom model ARN
        2. Lambda-SQS UUID

3. ### Create the Shutdown Lambda Function:
    1. From the Lambda console, click on Create Function (follow steps from the previous section):
    2. Add the Function Name and Runtime, click create Function:
    4. Import code from shutdown_function.py (refer code_sample folder in the repository) to the Lambda function. Ensure to replace the following paramters in the code :
        1. Rekognition custom model ARN
        2. Lambda-SQS UUID  
       
4. ### Configure EventBridge for Startup Lambda Function
    1. Search for EventBridge on the search bar in the management console and select EventBridge from the results.
       ![image (10)](https://github.com/aws-samples/rekognition-inference-scheduler/assets/32926625/724e5991-1a03-4c74-87e1-5d30d7b38188)
    2. Click on Create Rule:
       ![image (11)](https://github.com/aws-samples/rekognition-inference-scheduler/assets/32926625/b36f0d0d-4264-4659-b3be-04da91e0fd8b)
    3. Add the required details to create the rule
       ![image (12)](https://github.com/aws-samples/rekognition-inference-scheduler/assets/32926625/6026f974-f8cc-4078-85d1-5f283f2aff1c)
    4. Add cron expression based on your requirement. 
       ![image (13)](https://github.com/aws-samples/rekognition-inference-scheduler/assets/32926625/e6eca95b-7603-4237-8ed2-87e04af5c8db)
    5. The above pattern will trigger everyday at 8 AM UTC. Adjust the pattern based on your requirement and timezone.
    6. Select the lambda function as target
       ![image (14)](https://github.com/aws-samples/rekognition-inference-scheduler/assets/32926625/f6dfdcb3-c4f5-436d-a535-7179ad77360d)
    7. Choose Lambda function created in Step 2 from the dropdown.

5. ### Configure EventBridge for Shutdown Lambda Function
    1. Follow the above steps, change the shutdown time based on your requirement and select the lambda function created in step 3.















See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

