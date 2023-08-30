# Optimising Rekognition Custom Labels inferencing cost by shutting down during off-business hours

TODO: Fill this README out!

Be sure to:

* Change the title in this README
* Edit your repository description on GitHub

## Overview

Amazon Rekognition is a fully managed AI service provided by AWS. Amazon Rekognition makes it easy to add image and video analysis to your applications.

With Amazon Rekognition Custom Labels, you can identify the objects, logos, and scenes in images that are specific to your business needs. For example, you can find your logo in social media posts, identify your products on store shelves, classify machine parts in an assembly line, distinguish healthy and infected plants, or detect animated characters in images.

## Introduction:

Many solutions built on Rekognition Custom Labels require an inferencing only during the business hours which leads idle Rekognition inferencing instance after the business hours. For example, the SLA requires inferencing between 9AM and 5 PM everyday.

This AWS Github Sample will help you save on the inference cost for your Rekognition custom label models by scheduling the automatic shut down of the inferencing instance after office hours and turning it on as the workday starts.

## Initial Architecture:

![schdeuler_rekognition drawio](https://github.com/aws-samples/rekognition-inference-scheduler/assets/32926625/c25d586c-f7aa-49c8-b8c1-7195cdf99321)

Consider the usecase where the file to be inferenced on are uploaded to an S3 bucket and S3 event notification adds the newly uploaded objects to an SQS Queue. The queue is subscribed by a Lambda Function, that process and get inferencing result from the Rekognition Custom Label.

## Recommended Architecture for scheduling:

![schdeuler_rekognition drawio (1)](https://github.com/aws-samples/rekognition-inference-scheduler/assets/32926625/b4117a6a-115f-4969-9e41-8d291275883e)

## Workflow

1. EventBridge Scheduler Cronjob triggers the Startup Lambda function at the scheduled time. Ex. 8.30 AM.
2. Startup Lambda function makes the call to start the model using “start_project_version” API.
3. Startup Lambda function enables event source mapping for the source SQS queue and the Inference Lambda function.
4. Once the Rekognition Custom Label Model is live, Inference Lambda can start running inferencing for the uploaded items.
5. EventBridge Scheduler Cronjob will trigger the Shutdown function at the scheduled time (end of the day). Ex. 5.00 PM.
6. Shutdown Lambda Function will remove the event source mapping for the Inference function from the SQS queue.
7. Shutdown Lambda function makes the call to stop the model using “stop_project_version” API.




See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

