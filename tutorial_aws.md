# EB CONFIG
(FAZER EM ULTIMO)

ES_2425: cd banco
ES_2425/banco:

pip install -r requirements.txt

pip freeze > requirements.txt

(mudar as credenciais)
nano ~/.aws/credentials

eb init

eb create banco-env --service-role LabRole --keyname vockey --instance_profile LabInstanceProfile

eb deploy

eb terminate banco-env

# RDS 

Criar MySQL no RDS
{
    FREE TIER

    nome: algo-db

    admin
    pass automatica e mudar no models.py

    PUBLIC ACCESS
}

ATUALIZAR INFORMAÇÃO NO MODELS.PY

inserir dados por algum canto (dbeaver, terminal, whatever)

CREATE DATABASE users-info;

-- Create the clients table
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,             -- Auto-incrementing primary key
    username VARCHAR(150) NOT NULL,    -- Username field, max length 150
    email VARCHAR(255) UNIQUE NOT NULL, -- Email field, must be unique
    password VARCHAR(255) NOT NULL,    -- Password field, hashed
    hasPermissions BOOLEAN DEFAULT FALSE -- Permissions flag, default is FALSE
);

-- Insert some sample data
INSERT INTO clients (username, email, password, hasPermissions)
VALUES 
    ('Filipe', 'filipe@gmail.com', '123456', FALSE),
    ('Emanuel', 'Emanuel@gmail.com', '123456', FALSE),
    ('Ivo', 'ivo@gmail.com', '123456', TRUE);


-----
face rekognition (https://medium.com/cloudnloud/build-your-own-face-recognition-service-using-amazon-rekognition-c75919d7f66e)

NO TERMINAL DO AWS

[cloudshell-user@ip-10-130-84-97 ~]$ aws rekognition create-collection --collection-id caras --region us-east-1

[cloudshell-user@ip-10-130-84-97 ~]$ aws s3 mb s3://caras-images --region us-east-1

[cloudshell-user@ip-10-130-84-97 ~]$ aws dynamodb create-table --table-name caras_recognition --attribute-definitions AttributeName=RekognitionId,AttributeType=S --key-schema AttributeName=RekognitionId,KeyType=HASH  --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 --region us-east-1

criar trigger para lambda function (fazer igual link acima, lambda function chama se face recoknition algo)

correr imagens_recog/add_images.py para adicionar imagens


ELIMINAR TUDO NO FINAL!!!!
S3 BUCKET
DYNAMO
REKOGNITION COLLECTION ---> no link


SEGUIR O LINK EM GERAL É MELHOR