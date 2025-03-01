# Web Application using AWS Elastic Beanstalk

This project involves setting up a web application using AWS Elastic Beanstalk (EB) for deployment, Amazon RDS for database management, and AWS Rekognition for facial recognition. The application includes user management, loan processing, and interview scheduling functionalities.

⚠️ Warning: This project is not runnable as-is since the workflows, step functions, and Lambda functions were not saved. Additional configuration and implementation are required to make the application fully operational.

Authors
- Filipe Obrist
- Emanuel Pacheco
- Ivo Simões

## Project Context

This project was developed for the Service Engineering course, focusing on designing and deploying scalable and reliable web services using cloud technologies. The application integrates multiple AWS services to demonstrate end-to-end functionality, including database management, facial recognition, and serverless computing.

## Setup Instructions

### 1. Environment Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/MrBrodinha/ES_2425/
   cd banco
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Update AWS credentials**:
   ```bash
   nano ~/.aws/credentials
   ```

### 2. Elastic Beanstalk Deployment
1. **Initialize EB**:
   ```bash
   eb init
   ```

2. **Create EB environment**:
   ```bash
   eb create banco-env --service-role LabRole --keyname vockey --instance_profile LabInstanceProfile
   ```

3. **Deploy application**:
   ```bash
   eb deploy
   ```

4. **Terminate EB environment** (if needed):
   ```bash
   eb terminate banco-env
   ```

### 3. RDS Database Setup
1. **Create MySQL RDS instance**:
   - Use the AWS Management Console to create a MySQL RDS instance.
   - Set the instance name to `algo-db`.
   - Use the `admin` username and generate a password.
   - Enable public access.

2. **Update `models.py`**:
   - Update the database connection details in `models.py` to match the RDS instance.

3. **Create database and tables**:
   ```sql
   CREATE DATABASE users-info;

   CREATE TABLE users (
       id SERIAL PRIMARY KEY,
       username VARCHAR(150) NOT NULL,
       email VARCHAR(255) UNIQUE NOT NULL,
       password VARCHAR(255) NOT NULL,
       credit_score DECIMAL(15, 2) DEFAULT 0,
       hasPermissions BOOLEAN DEFAULT FALSE
   );

   CREATE TABLE loans (
       loan_id INT AUTO_INCREMENT PRIMARY KEY,
       user_id INT NOT NULL,
       yearly_income DECIMAL(15, 2) NOT NULL,
       amount DECIMAL(15, 2) NOT NULL,
       duration INT NOT NULL,
       monthly_payment DECIMAL(15, 2) NOT NULL,
       answer VARCHAR(255),
       created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
       amount_paid DECIMAL(15, 2) DEFAULT 0,
       loan_officer_id INT DEFAULT 0
   );

   CREATE TABLE interview_slot (
       id SERIAL PRIMARY KEY,
       loan_id INT NOT NULL,
       is_slot_chosen BOOLEAN NOT NULL DEFAULT FALSE,
       interview_day DATE NOT NULL,
       interview_hour TIME NOT NULL
   );
   ```

### 4. AWS Rekognition Setup
1. **Create Rekognition collection**:
   ```bash
   aws rekognition create-collection --collection-id caras --region us-east-1
   ```

2. **Create S3 bucket**:
   ```bash
   aws s3 mb s3://caras-images --region us-east-1
   ```

3. **Create DynamoDB table**:
   ```bash
   aws dynamodb create-table --table-name caras_recognition --attribute-definitions AttributeName=RekognitionId,AttributeType=S --key-schema AttributeName=RekognitionId,KeyType=HASH --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 --region us-east-1
   ```

4. **Add images to Rekognition**:
   - Run the `add_images.py` script to add images to the Rekognition collection.

## Additional Resources
- [AWS Rekognition Guide](https://medium.com/cloudnloud/build-your-own-face-recognition-service-using-amazon-rekognition-c75919d7f66e)

## Notes
- Ensure all AWS resources are properly terminated after use to avoid unnecessary charges.
- Regularly update the `requirements.txt` file with the latest dependencies.
