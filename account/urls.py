from django.urls import path
from . import views



app_name = 'account'

urlpatterns = [
    path('login', views.user_login, name='user_login'),
    path('register', views.user_register, name='user_register'),
    # path('checkotp', views.CheckOtpView.as_view(), name='check_otp'),
    path('logout', views.user_logout, name='user_logout'),
    # path('add/address', views.AddAddressView.as_view(), name='add_address'),
    # path('logout', views.user_logout, name='user_logout'),
]