# Generate presigned_url for the uploaded object
share_url = s3.generate_presigned_url(
  # Specify allowable operations
  ClientMethod='get_object',
  # Set the expiration time
  ExpiresIn=3600,  # 1 hour in seconds
  # Set bucket and shareable object's name
  Params={'Bucket': 'gid-staging', 'Key': 'final_report.csv'}
)

# Print out the presigned URL
print(share_url)


import pandas as pd

df_list = []

for file in response['Contents']:
    # For each file in response load the object from S3
    obj = s3.get_object(Bucket='gid-requests', Key=file['Key'])
    # Load the object's StreamingBody with pandas
    obj_df = pd.read_csv(obj['Body'])
    # Append the resulting DataFrame to list
    df_list.append(obj_df)

# Concat all the DataFrames with pandas
df = pd.concat(df_list)

# Preview the resulting DataFrame
print(df.head())


# Generate an HTML table with no border and selected columns
services_df.to_html('./services_no_border.html',
           # Keep specific columns only
           columns=['service_name', 'link'],
           # Set border
           border=0)

# Generate an HTML table with border and all columns.
services_df.to_html('./services_border_all_columns.html', 
           border=1,        # Set border to 1
           escape=False)    # Set escape to False to allow HTML in links


# Upload the lines.html file to S3
s3.upload_file(Filename='lines.html', 
               # Set the bucket name
               Bucket='datacamp-public', Key='index.html',
               # Configure uploaded file
               ExtraArgs = {
                 # Set proper content type
                 'ContentType': 'text/html',
                 # Set proper ACL
                 'ACL': 'public-read'})

# Print the S3 Public Object URL for the new file.
print("http://{}.s3.amazonaws.com/{}".format('datacamp-public', 'index.html'))


import pandas as pd

df_list = []  # List to hold all the DataFrames

# Load each object from S3
for file in request_files:
    # Download the file from S3
    s3_day_reqs = s3.get_object(Bucket='gid-requests', Key=file['Key'])
    
    # Read the DataFrame from the S3 file and append it to df_list
    day_reqs = pd.read_csv(s3_day_reqs['Body'])  # 'Body' is the key for file content
    df_list.append(day_reqs)

# Concatenate all DataFrames in the list
all_reqs = pd.concat(df_list, ignore_index=True)

# Preview the concatenated DataFrame
all_reqs.head()



# Write agg_df to a CSV and HTML file with no border
agg_df.to_csv('./feb_final_report.csv')
agg_df.to_html('./feb_final_report.html', border=0)

# Upload the generated CSV to the gid-reports bucket
s3.upload_file(Filename='./feb_final_report.csv', 
	Key='2019/feb/final_report.html', Bucket='gid-reports',
    ExtraArgs  = {'ACL': 'public-read'})

# Upload the generated HTML to the gid-reports bucket
s3.upload_file(Filename='./feb_final_report.html', 
	Key='2019/feb/final_report.html', Bucket='gid-reports',
    ExtraArgs  = {'ContentType': 'text/html', 
                 'ACL': 'public-read'})




# Assume s3 variable is already created as a boto3 S3 client
s3 = boto3.client('s3')

# List the gid-reports bucket objects starting with 2019/
objects_list = s3.list_objects(Bucket='gid-reports', Prefix='2019/')
objects_df = pd.DataFrame(objects_list['Contents'])

# Check if the response contains 'Contents'
if 'Contents' in objects_list:
    # Convert the response contents to DataFrame
    
    
    # Create a column "Link" that contains Public Object URL
    base_url = "http://gid-reports.s3.amazonaws.com/"
    objects_df['Link'] = base_url + objects_df['Key']  # Use 'Key' instead of '____'

    # Preview the resulting DataFrame
    print(objects_df.head())
else:
    print("No objects found in the specified bucket and prefix.")



    # Ensure 'Link' column contains clickable links by converting them into <a> tags
# objects_df['Link'] = objects_df['Link'].apply(lambda x: f'<a href="{x}">{x}</a>')

# Write objects_df to an HTML file
objects_df.to_html('report_listing.html',
                   index=False,    # Remove index column
                  #  escape=False,   # Allow for HTML rendering (links will render correctly)
                   columns=['Link', 'LastModified', 'Size'],
                   render_links=True
                   )  # Only include specific columns

# Overwrite the 'index.html' file in the S3 bucket
s3.upload_file(
    Filename='./report_listing.html', Key='index.html', 
    Bucket='gid-reports',
    ExtraArgs={
        'ContentType': 'text/html', 
        'ACL': 'public-read'
    })



