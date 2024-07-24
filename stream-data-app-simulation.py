import boto3
import csv
import json
from time import sleep
from datetime import datetime

session= boto3.Session()


s3 = session.client('s3', region_name='ap-south-1')
s3_resource = session.resource('s3', region_name='ap-south-1')
kinesis_client = session.client('kinesis', region_name='ap-south-1')


kinesis_stream_name = 'ecommerce-raw-user-activity-stream-1'
streaming_partition_key = 'category_id'


def stream_data_simulator(input_s3_bucket, input_s3_key):
    s3_bucket = input_s3_bucket
    s3_key = input_s3_key

    csv_file = s3_resource.Object(s3_bucket, s3_key)
    s3_response = csv_file.get()
    lines = s3_response['Body'].read().decode('utf-8').split('\n')

    for row in csv.DictReader(lines):
        try:
            
            line_json = json.dumps(row)
            json_load = json.loads(line_json)

            
            json_load['txn_timestamp'] = datetime.now().isoformat()
            

            response = kinesis_client.put_record(StreamName=kinesis_stream_name, Data=json.dumps(json_load, indent=4),
                                                 PartitionKey=str(json_load[streaming_partition_key]))
            
            print('HttpStatusCode:', response['ResponseMetadata']['HTTPStatusCode'], ', ', json_load['category_code'])

            sleep(0.250)

        except Exception as e:
            print('Error: {}'.format(e))


for i in range(0, 5):
    stream_data_simulator(input_s3_bucket="ecommerce-raw-apsouth1-144025787116-dev",
                          input_s3_key="ecomm_user_activity_sample/2019-Nov-sample.csv")
