"""
Sending an alert
Elena Block, Sam's old friend and council member is running for office and potholes are a big deal in her district. She wants to help fix it.
Elena asked Sam to adjust the streets_critical topic to send an alert if there are over 100 unfixed potholes in the backlog.
Sam has created the boto3 SNS client in the sns variable. She stored the streets_critical topic ARN in the str_critical_arn variable.
Help Sam take the next step.
She needs to check the current backlog count and send a message only if it exceeds 100.
The fate of District 12, and the results of Elena's election rest on your and Sam's shoulders.

If there are over 100 potholes, send a message with the current backlog count.
Create the email subject to also include the current backlog counit.
Publish message to the streets_critical Topic ARN."""

# If there are over 100 potholes, create a message
if streets_v_count > 100:
    # The message should contain the number of potholes
    message = "There are {} potholes!".format(streets_v_count)
    # The email subject should also contain the number of potholes
    subject = "Latest pothole count is {}".format(streets_v_count)

    # Publish the email to the streets_critical topic
    sns.publish(
        TopicArn=str_critical_arn,
        Message=message,     # Set message content
        Subject=subject      # Set email subject
    )
#*******************************************************

"""Sending a single SMS message
Elena asks Sam outside of work (per regulation) to send some thank you SMS messages to her largest donors.
Sam believes in Elena and her goals, so she decides to help.
She decides writes a quick script that will run through Elena's contact list and send a thank you text.
Since this is a one-off run and Sam is not expecting to alert these people regularly, there's no need to create a topic and subscribe them.
Sam has created the boto3 SNS client and stored it in the sns variable. The contacts variable contains Elena's contacts as a DataFrame.
Help Sam put together a quick hello to Elena's largest supporters!

Instructions:
For every contact, send an ad-hoc SMS to the contact's phone number.
The message sent should include the contact's name."""

# Loop through every row in contacts
for idx, row in contacts.iterrows():
    
    # Publish an ad-hoc sms to the user's phone number
    response = sns.publish(
        # Set the phone number
        PhoneNumber = str(row['Phone']),
        # The message should include the user's name
        Message = 'Hello {}'.format(row['Name'])
    )
   
    print(response)

#******************************************

