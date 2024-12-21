from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from app.serializers import UserSerializer

import boto3
import uuid

# AWS Config
Step_function_LoanResult_arn = 'arn:aws:states:us-east-1:471112572365:stateMachine:LoanResult'
Step_function_client = boto3.client(
    'stepfunctions',
    # aws_access_key_id='ASIAW3MD7LXGZUENADQQ',
    # aws_secret_access_key='hGpxwHiflvbOm0PLiKBuXyX/uN+15BPB3fT/a8o3',
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
    # we must define this still
    monthly_payment = (amount * 1.05) / duration  # Simple 5% interest calculation
    return Response({"monthly_payment": round(monthly_payment, 2)})

# Loan application submission
@api_view(['POST'])
def loan_apply(request):
    income = float(request.data.get('income'))
    expenses = float(request.data.get('expenses'))

    # Simulate credit score calculation based on income and expenses
    credit_score = int((income - expenses) / 100)

    print(f"Credit score: {credit_score}")

    # Create a unique execution name for Step Functions
    execution_name = f"loan-{uuid.uuid4()}"

    # Start Step Functions execution
    try:
        response = Step_function_client.start_execution(
            stateMachineArn=Step_function_LoanResult_arn,
            name=execution_name,
            input=f'{{"creditScore": {credit_score}}}'
        )
        return Response({
            "message": "Loan application submitted successfully!",
            "executionArn": response["executionArn"]
        })
    except Exception as e:
        print("An error occured: ", e)
        return Response({"error": str(e)}, status=500)
    
@api_view(['GET'])
def get_loan_result(request):
    execution_arn = request.query_params.get("executionArn")

    if not execution_arn:
        return Response({"error": "executionArn is required"}, status=400)

    # Get Step Functions execution result
    try:
        response = Step_function_client.describe_execution(
            executionArn=execution_arn
        )
        return Response({
            "status": response["status"],
            "result": response.get("output")  # Output from the workflow
        })
    except Exception as e:
        return Response({"error": str(e)}, status=500)

def test(request):
    return render(request, 'test.html')