import boto3

# Initialize the boto3 S3 resource
s3 = boto3.resource('s3')

# List of images and associated names
images = [
    ('imagem1.jpg', 'Ivo'),
    ('imagem2.jpg', 'Ivo'),
    ('imagem3.jpg', 'Ivo'),
    ('imagem4.jpg', 'Filipe'),
    ('imagem5.jpg', 'Filipe'),
    ('imagem6.jpg', 'Filipe'),
    ('emanuel1.jpg', 'Emanuel'),
    ('emanuel2.jpg', 'Emanuel'),
    ('emanuel3.jpg', 'Emanuel'),
    ('emanuel4.jpg', 'Emanuel'),
    ('emanuel5.jpg', 'Emanuel'),
    ('emanuel6.jpg', 'Emanuel'),
    ('emanuel7.jpg', 'Emanuel'),
    ('emanuel8.jpg', 'Emanuel')
]

# Define the S3 bucket name
bucket_name = 'caras-images'

for image in images:
    file = open(image[0],'rb')
    object = s3.Object('caras-images','index/'+ image[0])
    ret = object.put(Body=file,
                    Metadata={'username':image[1]})
