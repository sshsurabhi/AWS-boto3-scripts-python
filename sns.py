'''
Creating a Topic
Sam has been doing such a great job with her new skills, she got a promotion.
With her new title of Information Systems Analyst 3 (as opposed to 2), she has gotten a tiny pay bump in exchange for a lot more work.
Knowing what she can do, the City Council asked Sam to prototype an alerting system that will alert them when any department has more than 100 Get It Done requests outstanding.
They would like for council members and department directors to receive the alert.
Help Sam use her new knowledge of Amazon SNS to create an alerting system for Council!

Initialize the boto3 client for SNS.
Create the 'city_alerts' topic and extract its topic ARN.
Re-create the 'city_alerts' topic and extract its topic ARN with a one-liner.
Verify the two topic ARNs match.
'''
import boto3
# Initialize boto3 client for SNS
sns = boto3.client('sns',  # Specify the service name 'sns' for Simple Notification Service
                   region_name='us-east-1', 
                   aws_access_key_id=AWS_KEY_ID, 
                   aws_secret_access_key=AWS_SECRET)

# Create the city_alerts topic
response = sns.create_topic(Name="city_alerts")
c_alerts_arn = response['TopicArn']  # Extract the ARN of the created topic

# Re-create the city_alerts topic using a one-liner
c_alerts_arn_1 = sns.create_topic(Name='city_alerts')['TopicArn']

# Compare the two to make sure they match
print(c_alerts_arn == c_alerts_arn_1)

# **********************************************
"""
Creating multiple topics

Sam suddenly became a black sheep because she is responsible for an onslaught of text messages and notifications to department directors.
No one will go to lunch with her anymore!
To fix this, she decided to create a general topic per department for routine notifications, and a critical topic for urgent notifications.
Managers will subscribe only to critical notifications, while supervisors can monitor general notifications.
For example, the streets department would have 'streets_general' and 'streets_critical' as topics.
She has initialized the SNS client and stored it in the sns variable.
Help Sam create a tiered topic structure… and have friends again! 

For every department, create a general topic.
For every department, create a critical topic.
Print all the topics created in SNS
"""

# Create list of departments
departments = ['trash', 'streets', 'water']

for dept in departments:
    # For every department, create a general topic
    sns.create_topic(Name="{}_general".format(dept))
    
    # For every department, create a critical topic
    sns.create_topic(Name="{}_critical".format(dept))

# Print all the topics in SNS
response = sns.list_topics()
print(response['Topics'])


# ******************************************************

"""
Deleting multiple topics
It's hard to get things done in City government without good relationships. Sam is burning bridges with the general topics she created in the last exercise.
People are shunning her because she is blowing up their phones with notifications.
She decides to get rid of the general topics per department completely, and keep only critical topics.
Sam has created the boto3 client for SNS and stored it in the sns variable.
Help Sam regain her status in the bureaucratic social hierarchy by removing any topics that do not have the word critical in them.

Get the current list of topics.
For every topic ARN, if it doesn't have the word 'critical' in it, delete it.
Print the list of remaining critical topics.
"""

# Get the current list of topics
topics = sns.list_topics()['Topics']

for topic in topics:
    # For each topic, if it is not marked critical, delete it
    if "critical" not in topic['TopicArn']:
        sns.delete_topic(TopicArn=topic['TopicArn'])

# Print the list of remaining critical topics
print(sns.list_topics()['Topics'])

#**************************************************************

