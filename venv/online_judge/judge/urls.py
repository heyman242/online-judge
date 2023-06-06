from django.urls import path
from . import views

app_name = 'judge'

urlpatterns = [
    path('', views.main, name='main'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('questions/', views.questions, name='questions'),
    path('questions/details/<int:id>/', views.details, name='details'),
    path('create-code-snippet/<int:id>/', views.create_code_snippet, name='create_code_snippet'),
    path('create-code-snippet/<int:id>/result/', views.result, name='result'),

]
