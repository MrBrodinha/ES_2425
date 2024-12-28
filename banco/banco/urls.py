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
from django.urls import include, path, re_path
from rest_framework import routers

from app import views

from django.views.generic import TemplateView

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # react
    path('', TemplateView.as_view(template_name='index.html')),

    # api
    path("api/login", views.login, name="login"),
    path("api/loans", views.get_loans, name="get_loans"),
    path("api/loan/simulate", views.loan_simulate, name="loan_simulate"),
    path("api/loan/apply", views.loan_apply, name="loan_apply"),
    path("api/loan/verify_face", views.verify_face, name="verify_face"),
    path("api/loan/submit_documents", views.submit_documents, name="submit_documents"),
    path("api/loan/pay", views.update_loan_amount_paid, name="update_loan_amount_paid"),
    path("api/loan/interviews", views.get_interviews, name="get_interviews"),
    path("api/loan/interviews/chosen", views.choose_interview_slot, name="choose_interview_slot"),
    path("api/loan/assign", views.update_loan_status, name="update_loan_status"),
    path("api/verify", views.is_loan_officer, name="is_loan_officer"),
    path("api/loan_officer/loans", views.get_loans_by_officer, name="get_loans_by_officer"),
    path("api/users", views.get_users, name="get_users"),

    # react
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html'))
]