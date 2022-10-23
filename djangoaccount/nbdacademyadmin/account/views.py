from __future__ import print_function
from functools import partial
from multiprocessing import context
from socket import MsgFlag
import io
from django.contrib.auth import authenticate
from django.http import HttpResponse
from account.renderers import UserRenderer
from account.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer


from account.serializers import  SendPasswordResetEmailSerializer, UpdateDataSerializer, UpdateTableDataUserTypeSerializer, UserAllDataSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializers,UserLoginSerializer, UserChangePasswordSerializer

# generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.
class UserRegistrationView(APIView):
    # renderer class ko use karne per humko jub bhi postman ya frontend se galat request karenge to error show hoga.
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        # serializer class ko import karke uska use karke data ko UserRegistrationSerializer class me de rahe hai. 
        serializer = UserRegistrationSerializers(data=request.data)
        # serializer ke under validation function ko call karega is_valid jo data ayega wo valid hai ki nahi wo dekhenge 
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token ,'msg':'Registration successful'}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#****************************************************************************#
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        # serializer class ko import karke uska use karke data ko UserLoginSerializer class me de rahe hai
        serializer = UserLoginSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email = email, password = password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token,'msg':'login successful'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or password is not valid']}},status=status. HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#****************************************************************************#
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    # Anonimus User ko data access karne ka mauka nahi dega kahega kya Authenticated hai ki nahi check karega.
    # permission user ko data access ke liye token ko authenticate karega. 
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        print('request', request.user)
        serializer = UserProfileSerializer(request.user)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
#****************************************************************************#
class UserTeacherListData(APIView):
    renderer_classes = [UserRenderer]
    # Anonimus User ko data access karne ka mauka nahi dega kahega kya Authenticated hai ki nahi check karega.
    # permission user ko data access ke liye token ko authenticate karega. 
    def get(self, request, format=None):
        if request.method == 'GET':
            data = User.objects.filter(usertype = 'teacher')
            serializer = UserAllDataSerializer(data, context={'request': request}, many=True)
            print(serializer.data)
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#****************************************************************************#
class UserStudentListData(APIView):
    renderer_classes = [UserRenderer]
    # Anonimus User ko data access karne ka mauka nahi dega kahega kya Authenticated hai ki nahi check karega.
    # permission user ko data access ke liye token ko authenticate karega. 
    def get(self, request, format=None):
        if request.method == 'GET':
            data = User.objects.filter(usertype = 'student')
            serializer = UserAllDataSerializer(data, context={'request': request}, many=True)
            print(serializer.data)
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#*****************************************************************************#
class UpdateProfile(APIView):
    renderer_classes = [UserRenderer]
    def put(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        print('pythonData',pythondata)
        id = pythondata.get('id')
        print('id',id)
        stu = User.objects.get(id=id)
        print('stu',stu)
        serializer = UpdateDataSerializer(stu, data=pythondata)
        
        if serializer.is_valid():
            print('serialized validated',serializer.validated_data)
            user = serializer.save()
            # res = {'msg':'Data updated !!'}
            # json_data = JSONRenderer().render(res)    
            # print(json_data)
            token = get_tokens_for_user(user)
            return Response({'token':token ,'msg':'data Updated'}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        #     return HttpResponse( json_data, content_type = 'application/json')
        # json_data = JSONRenderer().render(serializer.errors)
        # return HttpResponse(json_data, content_type ='application/json')
#*****************************************************************************#
class UpdateTable(APIView):
    renderer_classes = [UserRenderer]
    def put(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        print('pythonData',pythondata)
        id = pythondata.get('id')
        print('id',id)
        stu = User.objects.get(id=id)
        print('stu',stu)
        serializer = UpdateTableDataUserTypeSerializer(stu, data=pythondata)
        
        if serializer.is_valid():
            print('serialized validated',serializer.validated_data)
            serializer.save()
            return Response({'msg':'data Updated'}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#*****************************************************************************#
class DeleteTableRow(APIView):
    renderer_classes = [UserRenderer]
    def delete(self, request, *args, **kwargs):
        
        json_data = request.body
        print(json_data)
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        print('pythonData',pythondata)
        id = pythondata.get('id', None)
        print(id)
        if id is not None:
            try:
                stu = User.objects.get(id=id)
            except User.DoesNotExist:
                res = {'msg': "User with this is does not exists"}
                json_data = JSONRenderer().render(res)
                
                return HttpResponse(json_data,content_type= "application/json")
            stu.delete()
            res = {'msg': "User has been deleted successfully"}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data,content_type= "application/json")
        res = {'msg': "Please Provide some id to delete the student"}
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data,content_type= "application/json")
        
        
#*****************************************#




#*****************************************************************************#
class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    # jub bhi request send karenge LogedIn user se password ke liye to yaha LoggedIn user ke token ko IsAuthenticated karega agar user ke pass token nahi hoga to postman me show hoga  "detail": "Authentication credentials were not provided."? 
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data = request.data, context={'user':request.user})
        # request.data ke alawa koi or data (request.user jub koi user logedIn) ho to use send karna ho serializer me to context ka use karte hai or data ko object ke form me key value pair me send karete hai.
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Changed Succesfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_Ok)
#****************************************************************************#
class SendPasswordResetEmailView(APIView):
    rendered_classes = [UserRenderer]
    # jub bhi form pe user jo bhi emailId dalega wo emailId request pe ayega or us EmailId pe hume emil bhejna hai.
    def post(self, request, format=None):
        print(request.data)
        serializer = SendPasswordResetEmailSerializer(data = request.data)
       # waise yaha raise_exception=True karne pe if condition or return me serializer.errors ki jaruwat nahi hai kyunki jub bhi koi unvalid serializer hoga to wahi se exception call ho jayega or koi bhi code aage exicute nahi hoga.
        serializer.is_valid(raise_exception=True)
        print(serializer.data)
        return Response({'msg':'password Reset link send. please check your Email'}, status=status.HTTP_200_OK)
#****************************************************************************#
    # after user clicked link in mail 
class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)


# ********************************************************************#

