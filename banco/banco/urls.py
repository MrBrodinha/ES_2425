"""
URL configuration for banco project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from rest_framework import routers

from app import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("index/", views.index, name="index"),
    path("api/login", views.login, name="login"),
    path("api/home", views.home, name="home"),
    path("api/register", views.register, name="register"),
    path("api/users", views.get_all_users, name="get_all_users"),
    path("api/loans", views.get_all_loans, name="get_all_loans"),
    path("api/loan/simulate", views.loan_simulate, name="loan_simulate"),
    path("api/loan/apply", views.loan_apply, name="loan_apply"),
    path("api/loan/status", views.loan_status, name="loan_status"),
    path("api/loan/update", views.update_loan_status, name="update_loan_status"),
    path("api/interview/select", views.select_interview_slot, name="select_interview_slot"),
    path("api/interview/set", views.set_interview_slots, name="set_interview_slots"),
    path("test/", views.test, name="test")
]