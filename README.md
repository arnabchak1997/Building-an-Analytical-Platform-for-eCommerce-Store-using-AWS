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
SQL, Python3
Services : <br>
AWS S3, AWS Glue, AWS Athena, AWS Cloud9, Apache Flink, Amazon Kinesis, Amazon SNS, AWS Lambda, Amazon CloudWatch, QuickSight, Apache Zepplin, Amazon DynamoDB, AWS Glue DataBrew

**Architecture:** <br>
![image](https://github.com/user-attachments/assets/6b7eea73-01ea-4de1-81a4-2739282d5930)

**Execution steps:** <br>

Creation of S3 bucket




