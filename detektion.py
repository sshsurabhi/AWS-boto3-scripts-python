"""Cat detector
Sam has been getting more and more challenging projects as a result of her popularity and success.

The newest request is from the animal control team. They want to receive notifications when an image comes in from the Get It Done application contains a cat. They can find feral cats and go rescue them. They provided her with two images that she can test her system with. One contains a cat, one does not. Both images are referenced in variables imagel and image2 respectively.
Sam has also created the boto3 Rekognition client in the rekog variable.
Help Sam use Rekognition to enable the animal control team to rescue stray cats!

Instructions:
Use the Rekognition client to detect the labels for image1. Return a maximum of 1 label.
"""
# Use Rekognition client to detect labels in the first image (image1)
image1_response = rekog.detect_labels(
    Image={'S3Object': {'Bucket': 'your-bucket-name', 'Name': image1}},  # Specify the image as an S3 object
    MaxLabels=1  # Limit to one label for the response
)

# Print the labels detected by Rekognition
print(image1_response['Labels'])
#****************************************

"""Multiple cat detector

After using the Cat Detector for a bit, the Animal Control team found that it was inefficient for them to pursue one cat at a time. It would be better if they could find clusters of cats.
They asked if Sam could add the count of cats detected to the message in the alerts they receive. They also asked her to lower the confidence floor, allowing the system to have more false positives.
"""
# Create an empty counter variable
cats_count = 0

# Iterate over the labels in the response
for label in response['Labels']:
    # Find the cat label and check for detected instances
    if label['Name'] == 'Cat':
        for instance in label['Instances']:
            # Only count instances with confidence > 85
            if instance['Confidence'] > 85:
                cats_count += 1

# Print the count of cats detected
print(cats_count)
#*********************************************************

"""
Parking sign reader

City planners have millions of images from truck cameras. Since the city does not keep a record of this data, parking regulations would be very valuable for planners to know.

Sam found detect_text() in the boto3 Rekognition documentation. She is going to use it to extract text out of the images City planners provided."""

# Create empty list of words
words = []

# Iterate over the TextDetections in the response dictionary
for text_detection in response['TextDetections']:
    # If TextDetection type is WORD, append it to words list
    if text_detection['Type'] == 'WORD':
        # Append the detected text
        words.append(text_detection['DetectedText'])

# Print out the words list
print(words)

#***************************************************************

"""Detecting language

The City Council is wondering whether it's worth it to build a Spanish version of the Get It Done application. There is a large Spanish speaking constituency, but they are not sure if they will engage. Building in multi-lingual translation complicates the system and needs to be justified.

They ask Sam to figure out how many people are posting requests in Spanish.

She has already loaded the CSV into the dumping_df variable and subset it to the following columns:

Help Sam quantify the demand for a Spanish version of the Get It Done application. Figure out how many requesters use Spanish and print the final result!

Instructions:
For each row in the DataFrame, detect the dominant language.
Count the total number of posts in Spanish."""

# For each dataframe row 
for index, row in dumping_df.iterrows():
    # Get the public description field
    description = dumping_df.loc[index, 'public_description']
    
    if description != '':
        # Detect language in the field content using Comprehend
        resp = comprehend.detect_dominant_language(Text=description)
        
        # Assign the top choice language to the 'lang' column
        dumping_df.loc[index, 'lang'] = resp['Languages'][0]['LanguageCode']

# Count the total number of Spanish posts
spanish_post_ct = len(dumping_df[dumping_df.lang == 'es'])

# Print the result
print("{} posts in Spanish".format(spanish_post_ct))
#************************************************************
"""Translating Get It Done requests
Often, Get it Done requests come in with multiple languages in the description. This is a challenge for many City teams. In order to review the requests, many city teams need to have a translator on staff, or hope they know someone who speaks the language.
The Streets director asked Sam to help. He wanted her to translate the Get It Done requests by running a job at the end of every day.
Sam decides to run the request through the AWS translate service. She has already loaded the CSV into the dumping_df variable and subset it to the following colimns:
Help Sam translate the requests to Spanish by running them through the AWS translate service!"""

# For each dataframe row
for index, row in dumping_df.iterrows():
    # Get the public_description into a variable
    description = dumping_df.loc[index, 'public_description']
    
    if description != '':
        # Translate the public description to English
        resp = translate.translate_text(
            Text=description,
            SourceLanguageCode='auto',  # Automatically detect the source language
            TargetLanguageCode='es'     # Translate to Spanish ('es')
        )
        
        # Store original language in original_lang column
        dumping_df.loc[index, 'original_lang'] = resp['SourceLanguageCode']
        
        # Store the translation in the translated_desc column
        dumping_df.loc[index, 'translated_desc'] = resp['TranslatedText']

# Preview the resulting DataFrame
dumping_df = dumping_df[['service_request_id', 'original_lang', 'translated_desc']]
dumping_df.head()
#*******************************************************

