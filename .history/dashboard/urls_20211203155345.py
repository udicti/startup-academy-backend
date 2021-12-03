from django.urls import path
import dashboard.views as views

urlpatterns = [
    path('', views.index, 'dash')
]

