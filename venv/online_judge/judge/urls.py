from django.urls import path
from . import views

app_name = 'judge'
urlpatterns = [
    path('', views.main, name='main'),
    path('questions/', views.questions, name='questions'),
    path('questions/details/<int:id>', views.details, name='details')

]
