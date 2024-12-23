from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from app.serializers import UserSerializer

import json

import boto3
import uuid

import time


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

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


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

@api_view(['GET'])
# login page
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.get(username=username)
        if user.check_password(password):
            return Response({'message': 'Login success'})
        else:
            return Response({'message': 'Login failed'})
    else:
        return Response({'message': 'Login failed'})
    

# create user
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return Response({'message': 'User created'})
    else:
        return Response({'message': 'User not created'})
    

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