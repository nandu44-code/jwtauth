from django.urls import path
from . views import Register,Login,UserView

urlpatterns = [
    path('register',Register.as_view()),
    path('login',Login.as_view()),
    path('user',UserView.as_view())
]
