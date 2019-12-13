from django.urls import path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import UserViewSet, Register


router = routers.SimpleRouter()
router.register('users', UserViewSet, base_name='users')
urlpatterns = router.urls
urlpatterns += [
    path('register/', Register.as_view(), name='register-view'),
    path('login/', views.obtain_auth_token)
]
