import boto3
import time
import json

def process_image_file_local(filename,min_confidence):
    try:
        with open(filename, 'rb') as fileinput:
            image = fileinput.read()
        client = boto3.client('rekognition')
        start_time = time.time()
        response = client.detect_labels(Image={'Bytes':image}, MinConfidence=min_confidence)
        end_time = time.time()
        labels = []
        for label in response['Labels']:
            if label['Name'] == 'Fox' or label['Name'] == 'Cat' or label['Name'] == 'Dog':
                labels.append({'Name':label['Name'],'Confidence':label['Confidence']})
        time_taken = end_time - start_time
        return {'image':photo,'labels':labels,'time':time_taken}
    except Exception as e:
        # print(e)
        return None

def process_image_file_s3(bucket, photo, min_confidence):
    client = boto3.client('rekognition')
    start_time = time.time()
    try:
        response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},MinConfidence=min_confidence)
        end_time = time.time()
        time_taken = end_time - start_time
        labels = []
        for label in response['Labels']:
            if label['Name'] == 'Fox' or label['Name'] == 'Cat' or label['Name'] == 'Dog':
                labels.append({'Name':label['Name'],'Confidence':label['Confidence']})
        return {'image':photo,'labels':labels,'time':time_taken}
    except Exception as e:
        # print(e)
        return None

def process_video_file_s3():
    pass

in_val = input('Stock (S) or Camera (C): ')
min_confidence = 50
if in_val in ('S', 's'):
    # local
    photos = [f'stock_images/fox{x}.jpg' for x in range(1,6)]
    for photo in photos:
        result = process_image_file_local(photo,min_confidence)
        if result is not None:
            label_str = ""
            for label in result['labels']:
                label_str += f"{label['Name']} ({label['Confidence']:.2f});"
            print(f"{result['image']}: {label_str} in {result['time']}s")
elif in_val in ('C', 'c'):
    # s3
    bucket = 'foxcat-images'
    photos = [f'Snapshot{x:06d}.png' for x in range(1,41)]
    for photo in photos:
        result = process_image_file_s3(bucket,photo,min_confidence)
        if result is not None:
            label_str = ""
            for label in result['labels']:
                label_str += f"{label['Name']} ({label['Confidence']:.2f});"
            print(f"{result['image']}: {label_str} in {result['time']}s")
else:
    print('Nothing to see here!') 
