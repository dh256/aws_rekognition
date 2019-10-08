import boto3
import time

def process_image_file_local(filename):
    with open(filename, 'rb') as fileinput:
        image = fileinput.read()
    client = boto3.client('rekognition')
    start_time = time.time()
    response = client.detect_labels(Image={'Bytes':image})
    end_time = time.time()
    for label in response['Labels']:
        if label['Name'] == 'Fox':
            print(f"{label['Name']}: {label['Confidence']}")
    print(f'Time taken: {end_time - start_time}')

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
    except:
        return None

def process_video_file_s3():
    pass

min_confidence = 10
bucket = 'foxcat-images'
photos = [f'Snapshot{x:06d}.png' for x in range(1,41)]
for photo in photos:
    result = process_image_file_s3(bucket,photo,min_confidence)
    if result is not None:
        label_str = ""
        for label in result['labels']:
            label_str += f"{label['Name']} ({label['Confidence']:.2f});"
        print(f"{result['image']}: {label_str}")

