from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt,datetime
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
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt',value=token,httponly=True)

        response.data = {
            'jwt':token
        }

        return response
    

class UserView(APIView):
    def get(self,request):
        token =request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unautheticated!')
        
        user = User.objects.filter(id=payload['id']).first()
        print(user.email)
        serializer = UserSerializer(user)

        return Response(serializer.data)
    
class UserLogOut(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message':'success'
        }

        return response