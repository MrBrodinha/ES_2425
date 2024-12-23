# EB CONFIG

ES_2425: cd banco
ES_2425/banco:

pip install -r requirements.txt

pip freeze > requirements.txt

(mudar as credenciais)
nano ~/.aws/credentials

eb init

eb create banco-env --service-role LabRole --keyname vockey --instance_profile LabInstanceProfile

eb deploy

eb terminate banco-env# ANTES DE COMEÇAR A TRABALHAR

## RDS 

Criar MySQL no RDS
{
    FREE TIER

    nome: users-info

    admin
    admin123_456

    PUBLIC ACCESS
}

criar DB chamada "users-info" (por terminal, dbeaver, whatever)

adicionar dados "muppet"

-- Create the database
CREATE DATABASE example_db;

-- Connect to the database
\c example_db;

-- Create the user table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,             -- Auto-incrementing primary key
    username VARCHAR(150) NOT NULL,    -- Username field, max length 150
    email VARCHAR(255) UNIQUE NOT NULL, -- Email field, must be unique
    password VARCHAR(255) NOT NULL,    -- Password field, hashed
    hasPermissions BOOLEAN DEFAULT FALSE -- Permissions flag, default is FALSE
);

-- Insert some sample data
INSERT INTO app_users (username, email, password, has_permissions)
VALUES 
    ('Filipe', 'filipe@gmail.com', '123456', FALSE),
    ('Emanuel', 'Emanuel@gmail.com', '123456', FALSE),
    ('Ivo', 'ivo@gmail.com', '123456', TRUE);