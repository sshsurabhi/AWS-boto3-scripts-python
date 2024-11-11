"""
Subscribing to topics
Many department directors are already receiving critical notifications.
Now Sam is ready to start subscribing City Council members.
She knows that they can be finicky, and elected officials are not known for their attention to detail or tolerance for failure.
She is nervous, but decides to start by subscribing the friendliest Council Member she knows. She got Elena Block's email and phone number.
Sam has initialized the boto3 SNS client and stored it in the sns variable.
She has also stored the topic ARN for streets_critical in the str_critical_arn variable.
Help Sam subscribe her first Council member to the streets_critical topic!

Subscribe Elena's phone number to the 'streets_critical' topic.
Print the SMS subscription ARN.
Subscribe Elena's email to the 'streets_critical topic.
Print the email subscription ARN.
"""

# Subscribe Elena's phone number to streets_critical topic
resp_sms = sns.subscribe(
  TopicArn=str_critical_arn, 
  Protocol='sms', 
  Endpoint="+16196777733"
)

# Print the SubscriptionArn for SMS
print(resp_sms['SubscriptionArn'])

# Subscribe Elena's email to streets_critical topic
resp_email = sns.subscribe(
  TopicArn=str_critical_arn, 
  Protocol='email', 
  Endpoint="eblock@sandiegocity.gov"
)

# Print the SubscriptionArn for email
print(resp_email['SubscriptionArn'])

#*****************************************

"""
Creating multiple subscriptions

After the successful pilot with Councilwoman Elena Block, other City Council members have been asking to be signed up for alerts too.
Sam decides that she should manage subscribers in a CSV file, otherwise she would lose track of who needs to be subscribed to what.
She creates a CSV named contacts and decides to subscribe everyone in the CSV to the streets_critical topic.
She has created the boto3 SNS client in the sns variable, and the streets_critical topic ARN is in the str_critical_arn variable.
Sam is going from being a social pariah to being courted by multiple council offices.
Help her solidify her position as master of all information by adding all the users in her CSV to the streets_critical topic!

For each element in the Email column of contacts, create a subscription to the 'streets_critical' Topic.
List subscriptions for the 'streets_critical' Topic and convert them to a DataFrame.
Preview the DataFrame.
"""

# For each email in contacts, create subscription to streets_critical
for email in contacts['Email']:
    sns.subscribe(
        TopicArn=str_critical_arn,
        Protocol='email',  # Set channel to 'email'
        Endpoint=email     # Set recipient to current email
    )

# List subscriptions for streets_critical topic and convert to DataFrame
response = sns.list_subscriptions_by_topic(TopicArn=str_critical_arn)
subs = pd.DataFrame(response['Subscriptions'])

# Preview the DataFrame
subs.head()
#*********************************************

"""
Deleting multiple subscriptions
Now that Sam has a maturing notification system, she is learning that the types of alerts she sends do not bode well for text messaging.
SMS alerts are great if the user can react that minute, but "We are 500 potholes behind" is not something that a Council Member can jump up and fix.
She decides to remove all SMS subscribers from the streets_critical topic, but keep all email subscriptions.
She created the boto3 SNS client in the sns variable, and the streets_critical topic ARN is in the str_critical_arn variable.
In this exercise, you will help Sam remove all SMS subscribers and make this an email only alerting system.

List subscriptions for 'streets_critical' topic.
For each subscription, if the protocol is 'sms', unsubscribe.
List subscriptions for 'streets_critical' topic in one line.
Print the subscriptions
"""
# List subscriptions for streets_critical topic
response = sns.list_subscriptions_by_topic(TopicArn=str_critical_arn)

# For each subscription, if the protocol is SMS, unsubscribe
for sub in response['Subscriptions']:
    if sub['Protocol'] == 'sms':
        sns.unsubscribe(SubscriptionArn=sub['SubscriptionArn'])

# List subscriptions for streets_critical topic in one line
subs = sns.list_subscriptions_by_topic(TopicArn=str_critical_arn)['Subscriptions']

# Print the subscriptions
print(subs)
#*******************************************

