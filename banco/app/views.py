from rest_framework import permissions, viewsets
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

import json

import boto3
import uuid

import time

from . import models
import jwt

import base64

import os

# AWS Config
Step_function_LoanResult_arn = 'arn:aws:states:us-east-1:975050165416:stateMachine:LoanResult'
Step_function_LoanSimulate_arn = 'arn:aws:states:us-east-1:975050165416:stateMachine:LoanSimulate'
Step_function_LoanStatus_arn = 'arn:aws:states:us-east-1:975050165416:stateMachine:LoanStatus'
Step_function_SelectInterviewSlot_arn = 'arn:aws:states:us-east-1:975050165416:stateMachine:SelectInterviewSlot'
Step_function_SetInterviewSlots_arn = 'arn:aws:states:us-east-1:975050165416:stateMachine:SetInterviewSlots'
Step_function_GetLoans_arn = 'arn:aws:states:us-east-1:975050165416:stateMachine:GetLoans'
Step_function_UdpateLoanStatus_arn = 'arn:aws:states:us-east-1:975050165416:stateMachine:UpdateLoanStatus'
Step_function_LoanResultRDS_arn = 'arn:aws:states:us-east-1:975050165416:stateMachine:LoanResultRDS'

Step_function_client = boto3.client(
    'stepfunctions',
    region_name='us-east-1'
)

rekognition = boto3.client(
    'rekognition', 
    region_name='us-east-1'
)

dynamodb = boto3.client(
    'dynamodb', 
    region_name='us-east-1'
)

s3 = boto3.client(
    's3',
    region_name='us-east-1'
)

#validate token
def validate_token(token):
    key = 'AlgoBueAleatoriolol'
    try:
        decoded = jwt.decode(token, key, algorithms='HS256')
        return True
    except jwt.ExpiredSignatureError:
        return False
    
#return token info
def get_token_info(token):
    key = 'AlgoBueAleatoriolol'
    try:
        decoded = jwt.decode(token, key, algorithms='HS256')
        return decoded
    except jwt.ExpiredSignatureError:
        return False

# get all users
@api_view(['GET'])
def get_all_users(request):
    users = User.objects.all()
    data = UserSerializer(users, many=True).data
    return Response(data)

@api_view(['GET'])
# index page
def index(request):
    data = { 'message': 'Hello 123' }
    return Response(data)

@api_view(['GET'])
# home page
def home(request):
    return Response({'message': 'Welcome to the home page'})

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    image = request.data.get('photo')

    client = models.get_client_by_email(email)

    if client is None:
        return Response({'message': 'User not found'})

    else:
        if client[3] == password:
            
            if ',' in image:
                image = image.split(',')[1]

            image_bytes = base64.b64decode(image)

            try:
                response = rekognition.search_faces_by_image(
                    CollectionId='caras',
                    Image={'Bytes':image_bytes}                                       
                )
            except Exception as e:
                return Response({'message': 'Face not found'})

            found = False

            for match in response['FaceMatches']:
                face = dynamodb.get_item(
                    TableName='caras_recognition',  
                    Key={'RekognitionId': {'S': match['Face']['FaceId']}}
                    )
                
                if 'Item' in face and face['Item']['FullName']['S'] == client[1]:
                    found = True
                    break

            if not found:
                return Response({'message': 'Person cannot be recognized'})

            token = {
                'id': client[0],
                'username': client[1],
                'email': client[2],
                'hasPermission': client[4]
            }

            key = 'AlgoBueAleatoriolol'

            #obtain token from token
            token = jwt.encode(token, key, algorithm='HS256')

            return Response({'username': f'{client[1]}',
                             'token': token}) 
        else:
            return Response({'message': 'Wrong password'})
        

@api_view(['POST'])
def verify_face(request):
    image = request.data.get('photo')
    token = request.data.get('token')

    if not validate_token(token):
        return Response({'message': 'Invalid token, please log out and log in again'})
    
    username = get_token_info(token)['username']

    if ',' in image:
        image = image.split(',')[1]

    image_bytes = base64.b64decode(image)

    try:
        response = rekognition.search_faces_by_image(
            CollectionId='caras',
            Image={'Bytes':image_bytes}                                       
        )

    except Exception as e:
        return Response({'message': 'Face not found'})
    
    found = False

    for match in response['FaceMatches']:
        face = dynamodb.get_item(
            TableName='caras_recognition',  
            Key={'RekognitionId': {'S': match['Face']['FaceId']}}
            )
        
        if 'Item' in face and face['Item']['FullName']['S'] == username:
            found = True
            return Response({'confirmation': 'correct'})
        
    if not found:
        return Response({'message': 'Person cannot be recognized'})

    
# Loan simulation endpoint
@api_view(['POST'])
def loan_simulate(request):
    amount = float(request.data.get('amount'))
    duration = int(request.data.get('duration'))
    yearly_income = float(request.data.get('yearly_income'))
    
    # Create a unique execution name
    execution_name = f"loan-{uuid.uuid4()}"

    # Start Step Functions execution
    response = Step_function_client.start_execution(
        stateMachineArn=Step_function_LoanSimulate_arn,
        name=execution_name,
        input=f'{{"amount":{amount},"duration":{duration},"yearly_income":{yearly_income}}}'
    )
    execution_arn = response["executionArn"]

    # Poll for execution result
    while True:
        execution_response = Step_function_client.describe_execution(
            executionArn=execution_arn
        )
        status = execution_response["status"]
        
        if status == "SUCCEEDED":
            # Parse the result
            result = execution_response["output"]
                
            return Response({
                "message": "Loan simulation processed successfully!",
                "Result": json.loads(result)
            })
        elif status in ["FAILED", "TIMED_OUT", "ABORTED"]:
            return Response({
                "error": f"Step Functions execution failed with status: {status}"
            }, status=500)
        
        # Wait before polling again
        time.sleep(2)

@api_view(['POST'])
def submit_documents(request):
    token = request.POST.get('token')
    if not validate_token(token):
        return Response({'message': 'Invalid token, please log out and log in again'})

    user_id = get_token_info(token)['id']

    last_loan_id = models.get_last_loan_id() + 1
    
    anual_income = request.FILES.get('annual_income')
    self_declaration = request.FILES.get('self_declaration')

    if anual_income is None or self_declaration is None:
        return Response({'message': 'Please upload all required documents'}, status=400)
    
    if anual_income.size > 1000000 or self_declaration.size > 1000000:
        return Response({'message': 'Files must not exceed 1 MB'}, status=400)
    
    # Upload the files to S3 irsplusdeclaration, create a folder with the user_id and upload the files there
    s3.upload_fileobj(anual_income, 'irsplusdeclaration', f'{user_id}/{last_loan_id}/anual_income.pdf')
    s3.upload_fileobj(self_declaration, 'irsplusdeclaration', f'{user_id}/{last_loan_id}/self_declaration.pdf')

    return Response({'confirmation': 'Documents submitted successfully!'})

# Loan application endpoint
@api_view(['POST'])
def loan_apply(request):
    token = request.data.get('token')
    if not validate_token(token):
        return Response({'message': 'Invalid token, please log out and log in, and try to apply for a loan again'})
    
    user_id = get_token_info(token)['id']

    try:
        # Extract income and expenses
        yearly_income = float(request.data.get('yearly_income'))
        amount = float(request.data.get('amount'))
        duration = int(request.data.get('duration'))
        monthly_payment = float(request.data.get('monthly_payment'))
        answer = request.data.get('answer')

        # Create a unique execution name
        execution_name = f"loan-{uuid.uuid4()}"

        # Start Step Functions execution
        response = Step_function_client.start_execution(
            stateMachineArn=Step_function_LoanResultRDS_arn,
            name=execution_name,
            input=f'{{"yearly_income": {yearly_income}, "amount": {amount}, "duration": {duration}, "monthly_payment": {monthly_payment}, "answer": "{answer}", "user_id": "{user_id}"}}'
        )
        execution_arn = response["executionArn"]

        # Poll for execution result
        while True:
            execution_response = Step_function_client.describe_execution(
                executionArn=execution_arn
            )
            status = execution_response["status"]
            
            if status == 200:
                return Response({
                    "confirmation": "Loan application processed successfully!"
                })
            elif status in ["FAILED", "TIMED_OUT", "ABORTED"]:
                return Response({
                    "error": f"Step Functions execution failed with status: {status}"
                }, status=500)

    except Exception as e:
        print("An error occurred: ", e)
        return Response({"error": str(e)}, status=500)

# Allows clients to check the status of their loan application.
@api_view(['GET'])
def loan_status(request):

    loan_id = request.GET.get('loan_id')
    
    # Create a unique execution name
    execution_name = f"loan-{uuid.uuid4()}"

    # Start Step Functions execution
    response = Step_function_client.start_execution(
        stateMachineArn=Step_function_LoanStatus_arn,
        name=execution_name,
        input=f'{{"loan_id": "{loan_id}"}}'
    )
    execution_arn = response["executionArn"]

    # Poll for execution result
    while True:
        execution_response = Step_function_client.describe_execution(
            executionArn=execution_arn
        )
        status = execution_response["status"]
        
        if status == "SUCCEEDED":
            # Parse the result
            result = execution_response["output"]
            return Response({
                "message": "Loan status processed successfully!",
                "Result": result
            })
        elif status in ["FAILED", "TIMED_OUT", "ABORTED"]:
            return Response({
                "error": f"Step Functions execution failed with status: {status}"
            }, status=500)
        
        # Wait before polling again
        time.sleep(2)

# Allows clients to select an interview slot.
@api_view(['POST'])
def select_interview_slot(request):
    loan_id = request.data.get('loan_id')
    slot_id = request.data.get('slot_id')

    # Create a unique execution name
    execution_name = f"loan-{uuid.uuid4()}"
    response = Step_function_client.start_execution(
        stateMachineArn=Step_function_SelectInterviewSlot_arn,
        name=execution_name,
        input=f'{{"loan_id": "{loan_id}", "slot_id": "{slot_id}"}}'
    )

    execution_arn = response["executionArn"]

    # Poll for execution result
    while True:
        execution_response = Step_function_client.describe_execution(
            executionArn=execution_arn
        )
        status = execution_response["status"]
        
        if status == "SUCCEEDED":
            # Parse the result
            result = execution_response["output"]
            return Response({
                "message": "Interview slot selected successfully!",
                "Result": result
            })
        elif status in ["FAILED", "TIMED_OUT", "ABORTED"]:
            return Response({
                "error": f"Step Functions execution failed with status: {status}"
            }, status=500)
        
        # Wait before polling again
        time.sleep(2)

@api_view(['POST'])
def set_interview_slots(request):
    slots = request.data.get('slots')
    loan_id = request.data.get('loan_id')

    # Example slots: ["2021-10-01T09:00:00", "2021-10-01T10:00:00", "2021-10-01T11:00:00"]

    print(f"Slots: {slots}")

    # Ensure slots is a valid list
    if not isinstance(slots, list):
        return Response({"error": "Slots must be a list."}, status=400)

    # Create a unique execution name
    execution_name = f"loan-{uuid.uuid4()}"

    # Properly serialize the input as JSON
    input_data = {
        "slots": slots,
        "loan_id": loan_id
    }

    # Convert input_data to a JSON string
    json_input = json.dumps(input_data)

    # Start the Step Function execution
    response = Step_function_client.start_execution(
        stateMachineArn=Step_function_SetInterviewSlots_arn,
        name=execution_name,
        input=json_input  # Pass the serialized JSON input
    )

    execution_arn = response["executionArn"]

    # Poll for execution result
    while True:
        execution_response = Step_function_client.describe_execution(
            executionArn=execution_arn
        )
        status = execution_response["status"]
        
        if status == "SUCCEEDED":
            # Parse the result
            result = execution_response["output"]
            return Response({
                "message": "Interview slots set successfully!",
                "Result": result
            })
        elif status in ["FAILED", "TIMED_OUT", "ABORTED"]:
            return Response({
                "error": f"Step Functions execution failed with status: {status}"
            }, status=500)
        
        # Wait before polling again
        time.sleep(2)

# Get all loans
@api_view(['GET'])
def get_all_loans(request):

    # Create a unique execution name
    execution_name = f"loan-{uuid.uuid4()}"

    # Start Step Functions execution
    response = Step_function_client.start_execution(
        stateMachineArn=Step_function_GetLoans_arn,
        name=execution_name,
        input='{}'
    )
    execution_arn = response["executionArn"]

    # Poll for execution result
    while True:
        execution_response = Step_function_client.describe_execution(
            executionArn=execution_arn
        )
        status = execution_response["status"]
        
        if status == "SUCCEEDED":
            # Parse the result
            result = execution_response["output"]
            return Response({
                "message": "Get Loans processed successfully!",
                "Result": result
            })
        elif status in ["FAILED", "TIMED_OUT", "ABORTED"]:
            return Response({
                "error": f"Step Functions execution failed with status: {status}"
            }, status=500)
        
        # Wait before polling again
        time.sleep(2)

# Update loan status
@api_view(['PUT'])
def update_loan_status(request):

    loan_id = request.data.get('loan_id')
    loan_status = request.data.get('loan_status')

    # Create a unique execution name
    execution_name = f"loan-{uuid.uuid4()}"

    # Start Step Functions execution
    response = Step_function_client.start_execution(
        stateMachineArn=Step_function_UdpateLoanStatus_arn,
        name=execution_name,
        input=f'{{"loan_id": "{loan_id}", "loan_status": "{loan_status}"}}'
    )

    execution_arn = response["executionArn"]

    # Poll for execution result
    while True:
        execution_response = Step_function_client.describe_execution(
            executionArn=execution_arn
        )
        status = execution_response["status"]
        
        if status == "SUCCEEDED":
            # Parse the result
            result = execution_response["output"]
            return Response({
                "message": "Loan status updated successfully!",
                "Result": result
            })
        elif status in ["FAILED", "TIMED_OUT", "ABORTED"]:
            return Response({
                "error": f"Step Functions execution failed with status: {status}"
            }, status=500)
        
        # Wait before polling again
        time.sleep(2)


def test(request):
    return render(request, 'test.html')