import boto3

# Initialize the boto3 S3 resource
s3 = boto3.resource('s3')

# List of images and associated names
images = [
    ('ivo1.jpg', 'Ivo'),
    ('ivo2.jpg', 'Ivo'),
    ('ivo3.jpg', 'Ivo'),
    ('emanuel1.jpg', 'Emanuel'),
    ('emanuel2.jpg', 'Emanuel'),
    ('emanuel3.jpg', 'Emanuel'),
    ('emanuel4.jpg', 'Emanuel'),
    ('emanuel5.jpg', 'Emanuel'),
    ('emanuel6.jpg', 'Emanuel'),
    ('emanuel7.jpg', 'Emanuel'),
    ('emanuel8.jpg', 'Emanuel'),
    ('filipe1.jpg', 'Filipe'),
    ('filipe2.jpg', 'Filipe'),
    ('filipe3.jpg', 'Filipe'),
    ('filipe4.jpg', 'Filipe'),
    ('filipe5.jpg', 'Filipe')
]

# Define the S3 bucket name
bucket_name = 'caras-images'

for image in images:
    file = open(image[0],'rb')
    object = s3.Object('caras-images','index/'+ image[0])
    ret = object.put(Body=file,
                    Metadata={'username':image[1]})
