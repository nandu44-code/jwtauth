from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
# Create your views here.

class Register(APIView):

    def post(self,request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class Login(APIView):
    def post(self,request):
        
        email = request.data['email']
        password = request.data['password']
        
        user = User.objects.get(email=email)

        if user is None:
            raise AuthenticationFailed('user not found')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        
        return Response(
            {
                'message':'success'
            }
        )