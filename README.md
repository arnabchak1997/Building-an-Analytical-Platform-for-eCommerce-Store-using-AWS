# Building-an-Analytical-Platform-for-eCommerce-Store-using-AWS

**Summary:** <br>
In this project, we will use an eCommerce dataset to simulate the logs of user purchases, product views, cart history, and the user’s journey on the online platform to create two analytical pipelines, Batch and Real-time. The Batch processing will involve data ingestion, Lake House architecture, processing, visualization using Amazon Kinesis, Glue, S3, and QuickSight to draw insights regarding the following: <br>
● Unique visitors per day <br>
● During a certain day, the users add products to their carts but don’t buy them <br>
● Top categories per hour or weekday (i.e. to promote discounts based on trends) <br>
● To know which brands need more marketing <br>
The Real-time channel involves detecting Distributed denial of service (DDoS) and Bot attacks using AWS Lambda, DynamoDB, CloudWatch, and AWS SNS. <br>

**Dataset Description:** <br>
This dataset has been taken for kaggle which contains user behavioral information from a large multi-category online store along with fields such as event_time, event_type, product_id, price, user_id. Each row in the file represents one of the following event types: <br>
● View <br>
● Cart <br>
● Removed from Cart <br>
● Purchase <br>

**Tech Stack:** <br>
Languages: <br>
SQL, Python3 <br>
Services : <br>
AWS S3, AWS Glue, AWS Athena, AWS Cloud9, Apache Flink, Amazon Kinesis, Amazon SNS, AWS Lambda, Amazon CloudWatch, QuickSight, Apache Zepplin, Amazon DynamoDB, AWS Glue DataBrew

**Architecture:** <br>
![image](https://github.com/user-attachments/assets/6b7eea73-01ea-4de1-81a4-2739282d5930)

**Execution steps:** <br>

**Creation of S3 bucket for storing raw dataset:** <br>

For this project, we are storing our raw data in the s3 bucket ecommerce-raw-apsouth1-144025787116-dev. For the real-time channel, we are using a sample of our entire dataset of a particular month's data i.e. 1000 records. We are using these 1000 records to simulate the user activity in the eCommerce store. The sample data is stored under ecommerce-raw-apsouth1-144025787116-dev/ecomm_user_activity_sample/. <br>
For the batch processing, we are using the entire month's dataset from kaggle and storing it under ecommerce-raw-apsouth1-144025787116-dev/ecomm_user_activity_uncompressed/ in a hive style partition of year and month. <br>

**Creation of Kinesis Data stream:** <br>

We are creating two kinesis datastream with on demand capacity -> ecommerce-raw-user-activity-stream-1/ecommerce-raw-user-activity-stream-2, ecommerce-raw-user-activity-stream-1 will be used to stream the real-time user acitivity data and ecommerce-raw-user-activity-stream-2 will be used to stream the aggregated user action data. <br>

**Creation of simulation app using boto3 and SDK:** <br>

In order to simulate the user activity data stored in s3 bukcet, we have created a simulation app in cloud9 using boto3 and SDK. This app is reading the s3 bucket ecommerce-raw-apsouth1-144025787116-dev/ecomm_user_activity_sample/ and iterating the records and sending them to ecommerce-raw-user-activity-stream-1 for streaming. With the record, we are also sending the current time stamp as transaction time stamp fo that record. We have used the category_id the streaming partition key. On successfully sending of a record to the data stream we are printing the http status code from the put record response metadata and the category id of the record sent. 

![image](https://github.com/user-attachments/assets/41edff61-66b7-4615-98e1-68f1aae6406c) <br>

**Creation of Kinesis data analytics environment:** <br>

The criteria that we are checking for DDos or bot attack is whether any user id is doing more than 10 actions in 10 seconds window. For that, we are aggregating our stream data from ecommerce-raw-user-activity-stream-1 and sending it to ecommerce-raw-user-activity-stream-2. For the purpose of this aggregation, we have created an Apache flink application using AWS Managed Flink service. 

First, we have created a streaming notebook ecommerce-streaming-app-v1 based on Apache Zeppelin with source stream as ecommerce-raw-user-activity-stream-1 and destination stream as ecommerce-raw-user-activity-stream-2 and the metadata for this is being stored in the database db_commerce in Glue catalog. The location for the code is provided as the s3 bucket ecommerce-raw-apsouth1-144025787116-dev/ecommerce-streaming-app-v1. Before running the notebook, we also need to add the Glueservice role to the IAM role for the streaming notebook so that it can access the database db_commerce in Glue catalog. <br>
From source stream ecommerce-raw-user-activity-stream-1, we are creating a table ecomm_user_activity_stream_1 and storing all the values of our record, in addition to that , we are creating a watermark over the transaction time stamp for an interval of 10 secs. We are creating another table ecomm_user_activity_stream_2 from the destination stream ecommerce-raw-user-activity-stream-2 where we are storing the user id and the count of that in the 10 secs interval. <br>
Now we build and export the notebook to upload it as a code archive in the s3 location we specified earlier while creation of the note book, then, we deployed this notebook as a flink kinesis analytics application with the source code that we created in the zeppelin notebook stored under ecommerce-raw-apsouth1-144025787116-dev/ecommerce-streaming-app-v1/zeppelin-code. <br>

![image](https://github.com/user-attachments/assets/bd8ad95e-ee64-4c68-971d-105fa33cd1f7) <br>

**Creation of Lambda function and processing the records from destination stream:** <br>

The lambda function will read the destination stream ecommerce-raw-user-activity-stream-2 and detect the DDos events as per the criteria we have set. We are creating a package by installing the aws_kinesis_agg library from which we are using the deaggregator function to deaggregate the records from the destination stream. The record from the destination stream is base64 encoded so we decode it and convert it to json format. Then we are sending the user id and the number of action per watermark to a Dynamo DB table. <br>

For DynamoDB table partition key we are using the nomenclature userid#{}#appserver#{} and for sort key we are using the current time stamp. Along with these we are sending these two fields in a cloudwatch metric. A SNS topic has been created where the lambda function will publish in case there are any user id detected which is doing more than 10 actions in an interval of 10 secs. An-email has been set as subscription for the SNS topic so everytime lambda publishes in the SNS topic, it will trigger an e-mail notification. 
<br>
We need to make sure that the lambda function IAM role has permission to Cloudwatch, Kinesis data stream and SNS. A trigger is created for the lambda function from kinesis so that whenever the destination stream ecommerce-raw-user-activity-stream-2 starts receiving the records from the flink application , it will invoke the function. <br>

**Running end-to-end real-time pipeline:** <br>

Since we have all the services configured , we can start running the pipeline. The simulation app in cloud9 environemnt is started which begins to send records to the source stream ecommerce-raw-user-activity-stream-1 for streaming, the flink application starts analysing the input data stream and begins to send the aggregated data to the sink which is the destination stream ecommerce-raw-user-activity-stream-2. <br>

![image](https://github.com/user-attachments/assets/501761b4-0f21-48a8-be69-92ad21e1706c)

The destination stream starts invoking the lambda function which will send the user_id and the num_of_actions_watermark data to the DynamoDB table. <br>

![image](https://github.com/user-attachments/assets/4c21e66e-54ed-4a2b-baa3-2122b9086adf) <br>

On successful processing of a record from destination stream, the lambda function is pushing logs in cloudwatch. <br>

![image](https://github.com/user-attachments/assets/768d3ff6-df13-479a-a556-2372e9945a08) <br>

Since our sample dataset did not have any user id with more than 10 actions in 10 secs interval, we created a test event in lambda which matches the criteria and ran it, the lambda function has published in the SNS topic which has triggered an e-mail. <br>

![image](https://github.com/user-attachments/assets/ed4b96cc-1c1a-4b7b-93d8-8d2c96439704) <br>

A backup of the source stream records is kept in a seperate s3 bukcet ecommerce-raw-stream-apsouth1-144025787116-dev. For this, we have used Amazon Data Firehose, the data stream ecommerce-raw-user-activity-stream-1 is selected as source and the s3 bucket ecommerce-raw-stream-apsouth1-144025787116-dev is tthe destination, buffer interval is kept 60 secs so every 60 secs firehose will be pushing the data to the s3 bucket. <br>

**ETL using Glue studio: ** <br>

For the batch processing part we are using the complete month's data , the data is unzipped and stored in s3 bucket location ecommerce-raw-apsouth1-144025787116-dev/ecomm_user_activity_uncompressed in hive style partiion of year and month. We created a crawler in Glue which will read this s3 location and create a table in database db_commerce in Glue catalog. In Glue studio, we created a small transformation job which converts the data to parquet format. For the transformation job , the source is selected as the data catalog table which the crawler created under database db_commerce. It will store the parquet format output data in location ecommerce-raw-apsouth1-144025787116-dev/ecomm_user_activity_parquet and also create a new table. The output data has been partitioned using the category id. 

**Visualization using Quicksight and Athena: ** <br>

We have the partitioned output data in parquet format in Glue catalog table, so we can use Athena to run SQL queries on that. For visualization , we are using Quicksight in this project. In Quicksight we have created three datasets with source as Athena. For one of the dataset , we are using the output table and for the remaining two datasets we have used custom SQL queries which we have used to draw insights like Unique visitors per day and During a certain day, the users add products to their carts but don’t buy them. Using Quicksight we have created the below visualizations as per the project aim. <br>

![Screenshot 2024-07-23 211805](https://github.com/user-attachments/assets/41c5b0c5-45af-4903-ab4b-4335b0d45132) <br>

![Screenshot 2024-07-23 211812](https://github.com/user-attachments/assets/0c37ec95-d93e-4b39-bab2-f37744af96fc) <br>

![Screenshot 2024-07-23 212016](https://github.com/user-attachments/assets/4ec8d555-4316-462a-ab27-024d3f80e0b0) <br>

![Screenshot 2024-07-23 211909](https://github.com/user-attachments/assets/985d473e-8ae6-4d1b-ad8c-c11e390f54b9) <br>

























