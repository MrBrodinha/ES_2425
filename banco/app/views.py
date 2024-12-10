from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from django.shortcuts import render

from app.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# get all users
def get_all_users(request):
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})

# index page
def index(request):
    return render(request, 'index.html')



