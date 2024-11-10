'''
Spring cleaning
Sam's pipeline has been running for a long time now. Since the beginning of 2018, her automated system has been diligently uploading her report to the gid-staging bucket.

In City governments, record retention is a huge issue, and many government officials prefer not to keep records in existence past the mandated retention dates.

As time has passed, the City Council asked Sam to clean out old CSV files from previous years that have passed the retention period. 2018 is safe to delete.

Sam has initialized the client and assigned it to the s3 variable. Help her clean out all records for 2018 from S3!

# List only objects that start with '2018/final_'
response = s3.____(Bucket='____', 
                           ____='2018/final_')

# Iterate over the objects
if 'Contents' in response:
  for obj in response['____']:
      # Delete the object
      s3.____(Bucket='____', Key=obj['Key'])

# Print the keys of remaining objects in the bucket
response = s3.____(____='gid-staging')

for obj in response['Contents']:
  	print(obj['____'])

List only objects that start with '2018/final_' in 'gid-staging' bucket.
Iterate over the objects, deleting each one.
Print the keys of remaining objects in the bucket.

'''

# List only objects that start with '2018/final_'
response = s3.list_objects(Bucket='gid-staging', Prefix='2018/final_')

# Iterate over the objects and delete each one
if 'Contents' in response:
    for obj in response['Contents']:
        # Delete the object
        s3.delete_object(Bucket='gid-staging', Key=obj['Key'])

# Print the keys of remaining objects in the bucket
response = s3.list_objects(Bucket='gid-staging')

for obj in response['Contents']:
    print(obj['Key'])


################################################# Upload the final_report.csv to gid-staging bucket
s3.upload_file(
    # Complete the filename
    Filename='./final_report.csv', 
    # Set the key and bucket
    Key='2019/final_report_2019_02_20.csv', 
    Bucket='gid-staging',
    # During upload, set ACL to public-read
    ExtraArgs={'ACL': 'public-read'}
)


# -------------------------------------
# List only objects that start with '2019/final_'
response = s3.list_objects(
    Bucket='gid-staging', Prefix='2019/final_')

# Iterate over the objects
for obj in response['Contents']:
  
    # Give each object ACL of public-read
    s3.put_object_acl(Bucket='gid-staging', 
                      Key=obj['Key'], 
                      ACL='public-read')
    
    # Print the Public Object URL for each object
    print("https://{}.s3.amazonaws.com/{}".format('gid-staging', obj['Key']))
    #########