import boto3
import base64
import time


with open('images/fox4.jpg', 'rb') as fileinput:
    jpeg = fileinput.read()

client = boto3.client('rekognition')

start_time = time.time()
response = client.detect_labels(Image={'Bytes':jpeg})
end_time = time.time()
for label in response['Labels']:
    if label['Name'] == 'Fox':
        print(f"{label['Name']}: {label['Confidence']}")
print(f'Time taken: {end_time - start_time}')
