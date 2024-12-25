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

# AWS Config
Step_function_LoanResult_arn = 'arn:aws:states:us-east-1:975050165416:stateMachine:LoanResult'
Step_function_LoanSimulate_arn = 'arn:aws:states:us-east-1:975050165416:stateMachine:LoanSimulate'
Step_function_LoanStatus_arn = 'arn:aws:states:us-east-1:975050165416:stateMachine:LoanStatus'
Step_function_SelectInterviewSlot_arn = 'arn:aws:states:us-east-1:975050165416:stateMachine:SelectInterviewSlot'
Step_function_SetInterviewSlots_arn = 'arn:aws:states:us-east-1:975050165416:stateMachine:SetInterviewSlots'
Step_function_GetLoans_arn = 'arn:aws:states:us-east-1:975050165416:stateMachine:GetLoans'
Step_function_UdpateLoanStatus_arn = 'arn:aws:states:us-east-1:975050165416:stateMachine:UpdateLoanStatus'

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

    

# Loan simulation endpoint
@api_view(['POST'])
def loan_simulate(request):
    amount = float(request.data.get('amount'))
    duration = int(request.data.get('duration'))
    
    # Create a unique execution name
    execution_name = f"loan-{uuid.uuid4()}"

    # Start Step Functions execution
    response = Step_function_client.start_execution(
        stateMachineArn=Step_function_LoanSimulate_arn,
        name=execution_name,
        input=f'{{"amount": {amount}, "duration": {duration}}}'
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
                "Result": result
            })
        elif status in ["FAILED", "TIMED_OUT", "ABORTED"]:
            return Response({
                "error": f"Step Functions execution failed with status: {status}"
            }, status=500)
        
        # Wait before polling again
        time.sleep(2)

# Loan application endpoint
@api_view(['POST'])
def loan_apply(request):
    try:
        # Extract income and expenses
        income = float(request.data.get('income'))
        expenses = float(request.data.get('expenses'))
        
        amount = float(request.data.get('amount'))
        duration = int(request.data.get('duration'))

        # user id
        user_id = request.data.get('user_id')

        # Simulate credit score calculation
        # credit_score = int((income - expenses) / 100)
        # print(f"Credit score: {credit_score}")

        # Create a unique execution name
        execution_name = f"loan-{uuid.uuid4()}"

        # Start Step Functions execution
        response = Step_function_client.start_execution(
            stateMachineArn=Step_function_LoanResult_arn,
            name=execution_name,
            input=f'{{"income": {income}, "expenses": {expenses}, "amount": {amount}, "duration": {duration}, "user_id": "{user_id}"}}'
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
                    "message": "Loan application processed successfully!",
                    "Result": result
                })
            elif status in ["FAILED", "TIMED_OUT", "ABORTED"]:
                return Response({
                    "error": f"Step Functions execution failed with status: {status}"
                }, status=500)
            
            # Wait before polling again
            time.sleep(2)

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