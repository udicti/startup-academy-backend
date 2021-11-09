
from django.urls import include, path
from rest_framework import routers
from udictidocs import views
from django.conf.urls.static import static
from django.conf.urls import url
# from django.conf import settings


urlpatterns = [
    # path('', include(router.urls)),
    path('selected_applicants_pdf/', views.selected_applicants_pdf_view, name="selected_applicants_pdf"),
    path('new_mem/', views.selected_applicants_pdf_view, name="selected_applicants_pdf"),
    
]

