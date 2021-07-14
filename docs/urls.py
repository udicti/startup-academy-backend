
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from applications import views
from django.conf.urls.static import static
from django.conf.urls import url
from django.conf import settings
from rest_framework_swagger.views import get_swagger_view


router = routers.DefaultRouter()
router.register(r'questions', views.ApplicationQuestionViewSet)
router.register(r'windows', views.ApplicationWindowsViewSet)
router.register(r'answers', views.AnswerViewSet)
router.register(r'applicants', views.ApplicantViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('applicant/', views.applicant.as_view()),
    path('answers/', views.answers.as_view()),
    path('windows/', views.windows.as_view()),
    path('update-reg/<uidb64>', views.editReg, name = "editReg"),
]

