# AWS_Rekognition

Example of using AWS Rekognition (Objects and Scenese) to recognise objects (labels) in an image.
AWS Rekognition will recognise a number of possible objects and scenes in an image. Each one is returned with a confidence indicator, any parent labels and any instances of the label. Any instances detected will have a Bounding Box of where object is in image.

Call detect_labels and examine return values.
Can either use byte array (Stock Images) or a S3 bucket (Camera Images) as source of image.

AWS Rekognition documentation: https://docs.aws.amazon.com/rekognition/
Pricing: https://aws.amazon.com/rekognition/pricing/