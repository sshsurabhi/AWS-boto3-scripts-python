"""Creating multi-level topics
The City Council asked Sam to create a critical and extreme topic for each department.
The critical topic will trigger alerts to staff and managers.
The extreme topics will trigger alerts to politicians and directors - it means the thresholds are completely exceeded.
For example, the trash department will have a trash_critical and trash_extreme topic.
She has already created the boto3 SNS client in the sns variable. She created a variable departments that contains a unique list of departments.
In this lesson, you will help Sam make the City run faster!
You will create multi-level topics with a different set of subscribers that trigger based on different thresholds.
You will effectively be building a smart alerting system!

Instructions:
For each department create a critical topic and store it in critical.
For each department, create an extreme topic and store it in extreme.
Place the created TopicArns into dept_arns.
Print the dictionary.
"""

# Initialize an empty dictionary to store the ARNs
dept_arns = {} 

for dept in departments:
  # For each department, create a critical topic
  critical = sns.create_topic(Name="{}_critical".format(dept))
  
  # For each department, create an extreme topic
  extreme = sns.create_topic(Name="{}_extreme".format(dept))
  
  # Store the created TopicARNs in the dictionary
  dept_arns['{}_critical'.format(dept)] = critical['TopicArn']
  dept_arns['{}_extreme'.format(dept)] = extreme['TopicArn']

# Print the filled dictionary to verify topics were created
print(dept_arns)
#******************************************************

"""Different protocols per topic level
Now that Sam has created the critical and extreme topics, she needs to subscribe the staff from her contact list into these topics.
Sam decided that the people subscribed to 'critical' topics will only receive emails. On the other hand, people subscribed to 'extreme' topics will receive SMS - because those are pretty urgent.
She has already created the boto3 SNS client in the sns variable.
Help Sam subscribe the users in the contacts DataFrame to email or SMS notifications based on their department. This will help get the right alerts to the right people, making the City of San Diego run better and faster!

Instructions:
Get the topic name by using the 'Department' field in the contacts DataFrame.
Use the topic name to create the critical and extreme TopicArns for a user's department.
Subscribe the user's email address to the critical topic.
Subscribe the user's phone number to the extreme topic.
"""

for index, user_row in contacts.iterrows():
  # Get topic names for the user's department
  critical_tname = '{}_critical'.format(user_row['Department'])
  extreme_tname = '{}_extreme'.format(user_row['Department'])
  
  # Get or create the TopicArns for the user's department.
  # For critical topic
  critical_arn = sns.create_topic(Name=critical_tname)['TopicArn']
  
  # For extreme topic
  extreme_arn = sns.create_topic(Name=extreme_tname)['TopicArn']
  
  # Subscribe each user's email to the critical Topic
  sns.subscribe(
    TopicArn=critical_arn, 
    Protocol='email', 
    Endpoint=user_row['Email']
  )
  
  # Subscribe each user's phone number for the extreme Topic
  sns.subscribe(
    TopicArn=extreme_arn, 
    Protocol='sms', 
    Endpoint=str(user_row['Phone'])
  )
#*************************************************************

"""Sending multi-level alerts
Sam is going to prototype her alerting system with the water data and the water department.
According to the Director, when there are over 100 alerts outstanding, that's considered critical. If there are over 300, that's extreme.
She has done some calculations and came up with a vcounts dictionary, that contains current requests for 'water', 'streets' and 'trash'.
She has also already created the boto3 SNS client and stored it in the sns variable.
In this exercise, you will help Sam publish a critical and an extreme alert based on the thresholds!

Instructions:
If there are over 100 water violations, publish to 'water_critical' topic.
If there are over 300 water violations, publish to 'water_extreme' topic."""

if vcounts['water'] > 100:
  # If over 100 water violations, publish to water_critical
  sns.publish(
    TopicArn = dept_arns['water_critical'],
    Message = "{} water issues".format(vcounts['water']),
    Subject = "Help fix water violations NOW!")

if vcounts['water'] > 300:
  # If over 300 violations, publish to water_extreme
  sns.publish(
    TopicArn = dept_arns['water_extreme'],
    Message = "{} violations! RUN!".format(vcounts['water']),
    Subject = "THIS IS BAD.  WE ARE FLOODING!")
  
#**********************************************************

"""Scooter dispatch
The City Council were huge fans of Sam's prediction about whether scooter was blocking a sidewalk or not. So much so, they asked her to build a notification system to dispatch crews to impound scooters from sidewalks.
With the dataset she created, Sam can dispatch crews to the case's coordinates when a request has negative sentiment.

Instructions:
Get the SNS topic ARN for 'scooter_notifications'.
For every row, if sentiment is 'NEGATIVE and there is an image of a scooter, construct a message to send.
Publish the notification to the SNS topic."""

# Get the SNS topic ARN for 'scooter_notifications'
topic_arn = sns.create_topic(Name='scooter_notifications')['TopicArn']

# Iterate over each row in the scooter_requests DataFrame
for index, row in scooter_requests.iterrows():
    # Check if the sentiment is 'NEGATIVE' and the image is of a scooter
    if (row['sentiment'] == 'NEGATIVE') & (row['img_scooter'] == True):  # Assuming True means there is an image of a scooter
        # Construct a message with coordinates and description
        message = "Please remove scooter at {}, {}. Description: {}".format(row['long'], row['lat'], row['public_description'])
        
        # Publish the message to the scooter team via the SNS topic
        sns.publish(TopicArn=topic_arn, Message=message, Subject="Scooter Alert")

#*******************************************************************

"""Getting request sentiment

After successfully translating Get It Done cases for the Streets Director, he asked for one more thing. He really wants to understand how people in the City feel about his department's work. She believes she can answer that question via sentiment analysis of Get It Done requests. She has already loaded the CSV into the dumping df variable and subset it to the following columns:

In this exercise, you will help Sam better understand the moods of the voices of the people that submit Get It Done cases, and whether they are coming into the interaction with the City in a positive mood or a negative one.

Instructions
Detect the sentiment of 'public_description' for every row.
Store the result in the 'sentiment' column."""

# For each dataframe row
for index, row in dumping_df.iterrows():
    # Get the public_description into a variable
    description = dumping_df.loc[index, 'public_description']
    
    if description != '':
        # Get the detect_sentiment response
        response = comprehend.detect_sentiment(
            Text=description,
            LanguageCode='en'  # Assuming the text is in English
        )
        
        # Get the sentiment value and store it in the 'sentiment' column
        dumping_df.loc[index, 'sentiment'] = response['Sentiment']

# Preview the dataframe
dumping_df.head()
#******************************************************************************

"""Scooter community sentiment

The City Council is curious about how different communities in the City are reacting to the Scooters. The dataset has expanded since Sam's initial analysis, and now contains Vietnamese, Tagalog, Spanish and English reports.

They ask Sam to see if she can figure it out. She decides that the best way to proxy for a community is through language (at least with the data she immediately has access to).
She has already loaded the CSV into the scooter df variable:

In this exercise, you will help Sam understand sentiment across many different languages. This will help the City understand how different communities are relating to scooters, something that will affect the votes of City Council members.

Instructions:
• For every DataFrame row, detect the dominant language.
• Like the detected language to determine the sentiment of the description
• Group the DataFrame bu the sentiment and Lane columns in that order."""

# For every DataFrame row
for index, row in scooter_requests.iterrows():
    # Get the public description for sentiment and language detection
    desc = scooter_requests.loc[index, 'public_description']
    
    if desc != '':
        # Detect the dominant language of the description
        resp = comprehend.detect_dominant_language(Text=desc)
        lang_code = resp['Languages'][0]['LanguageCode']
        
        # Store the detected language in the DataFrame
        scooter_requests.loc[index, 'lang'] = lang_code
        
        # Use the detected language to determine sentiment
        sentiment_response = comprehend.detect_sentiment(
            Text=desc,
            LanguageCode=lang_code
        )
        
        # Store the sentiment in the DataFrame
        scooter_requests.loc[index, 'sentiment'] = sentiment_response['Sentiment']

# Perform a count of sentiment by group (grouped by sentiment and language)
counts = scooter_requests.groupby(['sentiment', 'lang']).count()

# Display the result (count of descriptions by sentiment and language)
counts.head()
