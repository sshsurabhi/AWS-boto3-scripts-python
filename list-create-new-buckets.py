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

# Delete all the buckets with 'gim', create replacements.
for bucket in response['Buckets']:
    if 'gim' in bucket['Name']:
        s3.delete_bucket(Bucket=bucket['Name'])

# Create new buckets
s3.create_bucket(Bucket='gid-staging')
s3.create_bucket(Bucket='gid-processed')

# Print bucket listing after deletion
response = s3.list_buckets()
for bucket in response['Buckets']:
    print(bucket['Name'])