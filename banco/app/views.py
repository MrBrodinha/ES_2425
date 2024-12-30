from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import models
import json
import boto3
import uuid
import time
import jwt
import base64


# AWS Config
step_function_LoanResultRDS_arn = 'arn:aws:states:us-east-1:975050165416:stateMachine:LoanResultRDS'
step_function_LoanSimulate_arn = 'arn:aws:states:us-east-1:975050165416:stateMachine:LoanSimulate'
step_function_LoanStatus_arn = 'arn:aws:states:us-east-1:975050165416:stateMachine:LoanStatus'
step_function_SelectInterviewSlot_arn = 'arn:aws:states:us-east-1:975050165416:stateMachine:SelectInterviewSlot'
step_function_SetInterviewSlots_arn = 'arn:aws:states:us-east-1:975050165416:stateMachine:SetInterviewSlots'
step_function_GetLoans_arn = 'arn:aws:states:us-east-1:975050165416:stateMachine:GetLoans'
step_function_UdpateLoanStatus_arn = 'arn:aws:states:us-east-1:975050165416:stateMachine:UpdateLoanStatus'
step_function_UpdateLoanAmountPaid_arn = 'arn:aws:states:us-east-1:975050165416:stateMachine:UpdateLoanAmountPaid'
step_function_UpdateInterviewSlots_arn = 'arn:aws:states:us-east-1:975050165416:stateMachine:UpdateInterviewSlots'
step_function_UpdateLoanStatusRDS_arn = 'arn:aws:states:us-east-1:975050165416:stateMachine:UpdateLoanStatusRDS'
step_function_GetUsers_arn = 'arn:aws:states:us-east-1:975050165416:stateMachine:GetUsers'


step_function = boto3.client(
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

# Validates token
def validate_token(token):
    key = 'AlgoBueAleatoriolol'
    try:
        decoded = jwt.decode(token, key, algorithms='HS256')
        return True
    except jwt.ExpiredSignatureError:
        return False
    
# Returns token info
def get_token_info(token):
    key = 'AlgoBueAleatoriolol'
    try:
        decoded = jwt.decode(token, key, algorithms='HS256')
        return decoded
    except jwt.ExpiredSignatureError:
        return False

# Check if user is a loan officer
@api_view(['GET'])
def is_loan_officer(request):
    token = request.GET.get('token')

    if not validate_token(token):
        return Response({'message': 'Invalid token, please log out and log in again'})
    
    hasPermission = get_token_info(token)['hasPermissions']

    if hasPermission == 1:
        return Response({'is_loan_officer': True})
    else:
        return Response({'is_loan_officer': False})

# Logins user, by recieving an email, password and a photo
@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if (request.FILES.get('uploadedPhoto') != None):
        image = request.FILES.get('uploadedPhoto')

        image_bytes = image.read()
    else:
        image = request.data.get('photo')

        if ',' in image:
                image = image.split(',')[1]

        image_bytes = base64.b64decode(image)

    user = models.get_user_by_email(email)

    if user is None:
        return Response({'message': 'User not found'})

    else:
        if user[3] == password:

            try:
                response = rekognition.search_faces_by_image(
                    CollectionId='caras',
                    Image={'Bytes':image_bytes}                                       
                )
            except Exception as e:
                return Response({'message': e})

            found = False

            for match in response['FaceMatches']:
                face = dynamodb.get_item(
                    TableName='caras_recognition',  
                    Key={'RekognitionId': {'S': match['Face']['FaceId']}}
                    )
                
                if 'Item' in face and face['Item']['FullName']['S'] == user[1]:
                    found = True
                    break

            if not found:
                return Response({'message': 'Person cannot be recognized'})
            
            # expiration time
            exp = time.time() + 60*60*4

            token = {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'credit_score': float(user[4]),
                'hasPermissions': user[5],
                'exp': exp
            }

            key = 'AlgoBueAleatoriolol'

            #obtain token from token
            token = jwt.encode(token, key, algorithm='HS256')

            return Response({'username': f'{user[1]}',
                             'hasPermissions': user[5],
                             'token': token}) 
        else:
            return Response({'message': 'Wrong password'})
        

# Verifies face of person
@api_view(['POST'])
def verify_face(request):

    token = request.data.get('token')

    if not validate_token(token):
        return Response({'message': 'Invalid token, please log out and log in again'})
    
    if (request.FILES.get('uploadedPhoto') != None):
        image = request.FILES.get('uploadedPhoto')

        image_bytes = image.read()
    else:
        image = request.data.get('photo')

        if ',' in image:
                image = image.split(',')[1]

        image_bytes = base64.b64decode(image)
    
    username = get_token_info(token)['username']

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

    
# Simualates loan
@api_view(['POST'])
def loan_simulate(request):
    amount = float(request.data.get('amount'))
    duration = int(request.data.get('duration'))
    yearly_income = float(request.data.get('yearly_income'))
    
    # Create a unique execution name
    execution_name = f"loan-{uuid.uuid4()}"

    # Start Step Functions execution
    response = step_function.start_execution(
        stateMachineArn=step_function_LoanSimulate_arn,
        name=execution_name,
        input=f'{{"amount":{amount},"duration":{duration},"yearly_income":{yearly_income}}}'
    )
    execution_arn = response["executionArn"]

    # Poll for execution result
    while True:
        execution_response = step_function.describe_execution(
            executionArn=execution_arn
        )
        status = execution_response["status"]
        
        if status == "SUCCEEDED":
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

# Submits documents of a loan to S3 bucket
@api_view(['POST'])
def submit_documents(request):
    token = request.POST.get('token')
    if not validate_token(token):
        return Response({'message': 'Invalid token, please log out and log in again'})

    user_id = get_token_info(token)['id']

    last_load_id = models.get_last_loan_id()

    if last_load_id is None:
        loan_id = 1
    else:
        loan_id = last_load_id + 1
    
    anual_income = request.FILES.get('annual_income')
    self_declaration = request.FILES.get('self_declaration')

    if anual_income is None or self_declaration is None:
        return Response({'message': 'Please upload all required documents'}, status=400)
    
    if anual_income.size > 1000000 or self_declaration.size > 1000000:
        return Response({'message': 'Files must not exceed 1 MB'}, status=400)
    
    # Upload the files to S3 irsplusdeclaration, create a folder with the user_id and upload the files there
    s3.upload_fileobj(anual_income, 'irsplusdeclaration', f'{user_id}/{loan_id}/anual_income.pdf')
    s3.upload_fileobj(self_declaration, 'irsplusdeclaration', f'{user_id}/{loan_id}/self_declaration.pdf')

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

        if answer == "ACCEPTED":
            answer = "TO BE ACCEPTED"
        elif answer == "UNABLE TO DECIDE ALONE":
            answer = "WAITING FOR LOAN OFFICER"

        # Create a unique execution name
        execution_name = f"loan-{uuid.uuid4()}"

        # Start Step Functions execution
        response = step_function.start_execution(
            stateMachineArn=step_function_LoanResultRDS_arn,
            name=execution_name,
            input=f'{{"yearly_income": {yearly_income}, "amount": {amount}, "duration": {duration}, "monthly_payment": {monthly_payment}, "answer": "{answer}", "user_id": "{user_id}"}}'
        )
        execution_arn = response["executionArn"]

        # Poll for execution result
        while True:
            execution_response = step_function.describe_execution(
                executionArn=execution_arn
            )
            status = execution_response["status"]
            models.restart_connection()
            
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

# Allows clients to check the status of their loans application.
@api_view(['GET'])
def get_loans(request):
    token = request.GET.get('token', None)

    if not validate_token(token):
        return Response({'message': 'Invalid token, please log out and log in again'})
    
    loan_id = request.GET.get('loan_id', None)

    if loan_id is None:
        user_id = get_token_info(token)['id']
        loans_status = models.get_loans_by_user_id(user_id)

        if loans_status is None:
            return Response({'message': 'No loans found for this user.'})

        return Response({'loans_status': loans_status})
    
    else:
        loan_status = models.get_loan_by_id(loan_id)
        if loan_status is None:
            return Response({'message': 'No loan found with this id.'})

        return Response({'loan_status': loan_status})

# Updates amount paid to a loan
@api_view(['PUT'])
def update_loan_amount_paid(request):
    token = request.data.get('token')

    if not validate_token(token):
        return Response({'message': 'Invalid token, please log out and log in again'})

    loan_id = request.data.get('loan_id')

    # Create a unique execution name
    execution_name = f"loan-{uuid.uuid4()}"

    # Start Step Functions execution
    response = step_function.start_execution(
        stateMachineArn=step_function_UpdateLoanAmountPaid_arn,
        name=execution_name,
        input=f'{{"loan_id": "{loan_id}"}}'
    )

    execution_arn = response["executionArn"]

    # Poll for execution result
    while True:
        execution_response = step_function.describe_execution(
            executionArn=execution_arn
        )
        status = execution_response["status"]
        
        if status == "SUCCEEDED":
            # Parse the result
            result = execution_response["output"]

            models.restart_connection()

            return Response({
                "confirm": "Loan amount paid updated successfully!",
                "Result": result
            })
        elif status in ["FAILED", "TIMED_OUT", "ABORTED"]:
            return Response({
                "error": f"Step Functions execution failed with status: {status}"
            }, status=500)
        
        # Wait before polling again
        time.sleep(2)

# Retrives interviews from a loan
@api_view(['GET'])
def get_interviews(request):
    token = request.GET.get('token', None)

    if not validate_token(token):
        return Response({'message': 'Invalid token, please log out and log in again'})

    loan_id = request.GET.get('loan_id')

    interviews = models.get_slot_interviews_by_loan_id(loan_id)

    return Response({'interviews': interviews})

# Updates choosen interview
@api_view(['PUT'])
def choose_interview_slot(request):
    token = request.data.get('token')

    if not validate_token(token):
        return Response({'message': 'Invalid token, please log out and log in again'})
    
    loan_id = request.data.get('loan_id')
    interview_id = request.data.get('interview_id')

    models.update_loan_status_by_loan_id(loan_id, "INTERVIEW PENDING")

    # Create a unique execution name
    execution_name = f"loan-{uuid.uuid4()}"

    # Start Step Functions execution
    response = step_function.start_execution(
        stateMachineArn=step_function_UpdateInterviewSlots_arn,
        name=execution_name,
        input=f'{{"loan_id": "{loan_id}", "interview_id": "{interview_id}"}}'
    )

    execution_arn = response["executionArn"]

    # Poll for execution result
    while True:
        execution_response = step_function.describe_execution(
            executionArn=execution_arn
        )
        status = execution_response["status"]
        
        if status == "SUCCEEDED":
            # Parse the result
            result = execution_response["output"]

            models.restart_connection()

            return Response({
                "confirm": "Interview slot selected successfully!",
                "Result": result
            })
        elif status in ["FAILED", "TIMED_OUT", "ABORTED"]:
            return Response({
                "error": f"Step Functions execution failed with status: {status}"
            }, status=500)
        
        # Wait before polling again
        time.sleep(2)


# Updates loan status and links office loaner to it
@api_view(['PUT'])
def update_loan_status(request):
    token = request.data.get('token')

    if not validate_token(token):
        return Response({'message': 'Invalid token, please log out and log in again'})
    
    flag_officer = get_token_info(token)['hasPermissions']

    if flag_officer != 1:
        return Response({'message': 'You do not have permission to update loan status'})
    
    loan_id = request.data.get('loan_id')
    answer = request.data.get('answer')
    loan_officer_id = get_token_info(token)['id']

    # Create a unique execution name
    execution_name = f"loan-{uuid.uuid4()}"

    # Start Step Functions execution
    response = step_function.start_execution(
        stateMachineArn=step_function_UpdateLoanStatusRDS_arn,
        name=execution_name,
        input=f'{{"loan_id": "{loan_id}", "answer": "{answer}", "loan_officer_id": "{loan_officer_id}"}}'
    )

    execution_arn = response["executionArn"]

    # Poll for execution result
    while True:
        execution_response = step_function.describe_execution(
            executionArn=execution_arn
        )
        status = execution_response["status"]
        
        if status == "SUCCEEDED":
            # Parse the result
            result = execution_response["output"]

            models.restart_connection()

            return Response({
                "confirm": "Loan status updated successfully!",
                "Result": result
            })
        elif status in ["FAILED", "TIMED_OUT", "ABORTED"]:
            return Response({
                "error": f"Step Functions execution failed with status: {status}"
            }, status=500)
        
        # Wait before polling again
        time.sleep(2)


# Gets loans associated to loan officer
@api_view(['GET'])
def get_loans_by_officer(request):
    token = request.GET.get('token', None)
    loan_officer_id = request.GET.get('loan_officer_id', None)

    if (loan_officer_id == "1"):
        loan_officer_id = get_token_info(token)['id']

    if not validate_token(token):
        return Response({'message': 'Invalid token, please log out and log in again'})
    
    if get_token_info(token)['hasPermissions'] != 1:
        return Response({'message': 'You do not have permission to view unassigned loans'})

    loans = models.get_loans_by_officer_id(loan_officer_id)

    return Response({'loans': loans})


@api_view(['GET'])
def get_users(request):
    token = request.GET.get('token', None)

    if not validate_token(token):
        return Response({'message': 'Invalid token, please log out and log in again'})
    
    if get_token_info(token)['hasPermissions'] != 1:
        return Response({'message': 'You do not have permission to view users'})
    
    # Create a unique execution name
    execution_name = f"loan-{uuid.uuid4()}"

    # Start Step Functions execution
    response = step_function.start_execution(
        stateMachineArn=step_function_GetUsers_arn,
        name=execution_name,
        input='{}'
    )

    execution_arn = response["executionArn"]

    # Poll for execution result
    while True:
        execution_response = step_function.describe_execution(
            executionArn=execution_arn
        )
        status = execution_response["status"]
        
        if status == "SUCCEEDED":
            # Parse the result
            result = execution_response["output"]
            return Response({
                "users": result
            })
        elif status in ["FAILED", "TIMED_OUT", "ABORTED"]:
            return Response({
                "error": f"Step Functions execution failed with status: {status}"
            }, status=500)
        
        # Wait before polling again
        time.sleep(2)

@api_view(['GET'])
def get_single_user(request):
    token = request.GET.get('token', None)
    user_id = request.GET.get('user_id', None)
    loan_id = request.GET.get('loan_id', None)

    if not validate_token(token):
        return Response({'message': 'Invalid token, please log out and log in again'})
    
    if get_token_info(token)['hasPermissions'] != 1:
        return Response({'message': 'You do not have permission to view users'})
    
    user = models.get_user_by_id(user_id)

    anual_income_url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': 'irsplusdeclaration',
            'Key': f'{user_id}/{loan_id}/anual_income.pdf'
        }
    )

    self_declaration_url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': 'irsplusdeclaration',
            'Key': f'{user_id}/{loan_id}/self_declaration.pdf'
        },
        ExpiresIn=600
    )

    return Response({
        'user': {
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'credit_score': user[4]
        },
        'anual_income_url': anual_income_url,
        'self_declaration_url': self_declaration_url
    })

@api_view(['POST'])
def add_interview(request):
    token = request.data.get('token')

    if not validate_token(token):
        return Response({'message': 'Invalid token, please log out and log in again'})
    
    if get_token_info(token)['hasPermissions'] != 1:
        return Response({'message': 'You do not have permission to add interview slots'})
    
    loan_id = request.data.get('loan_id')
    interview_day = request.data.get('interview_day')
    interview_time = request.data.get('interview_time')

    models.add_slot_interview(loan_id, interview_day, interview_time)

    models.restart_connection()

    return Response({'confirmation': 'Interview slot added successfully!'})

@api_view(['DELETE'])
def remove_interview(request):
    token = request.data.get('token')

    if not validate_token(token):
        return Response({'message': 'Invalid token, please log out and log in again'})
    
    if get_token_info(token)['hasPermissions'] != 1:
        return Response({'message': 'You do not have permission to add interview slots'})
    
    slot_id = request.data.get('slot_id')

    models.remove_slot_interview(slot_id)

    models.restart_connection()

    return Response({'confirmation': 'Interview slot removed successfully!'})

@api_view(['DELETE'])
def remove_interviews_from_loan(request):
    token = request.data.get('token')

    if not validate_token(token):
        return Response({'message': 'Invalid token, please log out and log in again'})
    
    if get_token_info(token)['hasPermissions'] != 1:
        return Response({'message': 'You do not have permission to add interview slots'})
    
    loan_id = request.data.get('loan_id')

    models.remove_slots_interview_by_loan_id(loan_id)

    models.restart_connection()

    return Response({'confirmation': 'Interview slots removed successfully!'})