#Creating a bucket

import boto3

# Create boto3 client to S3
s3 = boto3.client('s3', region_name='us-east-1', 
                      aws_access_key_id=AWS_KEY_ID, 
                      aws_secret_access_key=AWS_SECRET)

# Create the buckets
response_staging = s3.create_bucket(Bucket='gim-staging')
response_processed = s3.create_bucket(Bucket='gim-processed')
response_test = s3.create_bucket(Bucket='gim-test')

# Print out the response for the 'gim-staging' bucket
print(response_staging)


# Get the list_buckets response
response = s3.list_buckets()

# Iterate over Buckets from .list_buckets() response
for bucket in response['Buckets']:
  
      # Print the Name for each bucket
    print(bucket['Name'])


    