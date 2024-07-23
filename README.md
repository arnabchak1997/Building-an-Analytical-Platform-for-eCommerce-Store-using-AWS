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

![image](https://github.com/user-attachments/assets/bd8ad95e-ee64-4c68-971d-105fa33cd1f7)






