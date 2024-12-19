from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from app.serializers import UserSerializer


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
    # Placeholder logic to randomly classify loan request
    result = ["Accept", "Interview", "Reject"]
    return Response({"result": result[0]})

def test(request):
    return render(request, 'test.html')