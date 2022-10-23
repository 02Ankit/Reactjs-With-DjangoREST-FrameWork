
from unittest.util import _MAX_LENGTH
from wsgiref import validate
from rest_framework import serializers
from account.models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Util

class UserRegistrationSerializers(serializers.ModelSerializer):
    # we are writing this becoz we need confirm password field in our Registration Request.
   # view se data UserRegistrationSerializer me aega or  validation hoga or return karega view me serializer variable ko.
    password2 = serializers.CharField(style = {'input_type':'password'}, write_only=True)
 
    class Meta:
        model = User
        # model se koun koun se field ka data lena hai 
        fields = ['email', 'firstname', 'lastname', 'contact', 'gender', 'usertype', 'password', 'password2', 'tc']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    # valiadate password and confirm password while registration
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and confirm Password doesn't match")
        return attrs
    
    # ek user create ho raha hai or humara model custome type isliye ek create method lagana padega 
    # pe generaly model custome type na ho to createmethod ki need nahi hoti
     
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
    # model serializer kam karta hai model form ki tarha.
    # view se data UserLoginSerializer me aega or default validation hoga or return karega view class me seializer variable ko.
    email =  serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']
        # serializer se data ko view me le ke authentication ka kam 
        # view me karenge.


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'firstname','lastname', 'contact', 'gender','usertype', 'is_admin']



class UserAllDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'firstname','lastname', 'contact', 'gender','usertype']




        
#*****************************************************************************#
class UpdateDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'email', 'firstname','lastname', 'contact']
    
    def update(self, instance, validated_data):
        instance.id = validated_data.get('id',instance.id)
        instance.email = validated_data.get('email',instance.email)
        instance.firstname = validated_data.get('firstname',instance.firstname)
        instance.lastname = validated_data.get('lastname',instance.lastname)
        instance.contact = validated_data.get('contact',instance.contact)
        print('instance of id',instance.id)
        print('instance of email',instance.email)
        print('instance of firstname',instance.firstname)
        print('instance of lastname',instance.lastname)
        print('instance of contact',instance.contact)
        instance.save()
        return instance 
   
#*****************************************************************************#
class UpdateTableDataUserTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'usertype']
    
    def update(self, instance, validated_data):
        instance.id = validated_data.get('id',instance.id)
        instance.usertype = validated_data.get('usertype',instance.usertype)
        
        print('instance of id',instance.id)
        print('instance of usertype',instance.usertype)
        
        instance.save()
        return instance 
#*****************************************************************************#
class UserChangePasswordSerializer(serializers.Serializer):
    #  yaha hum model Serializer ka use nahi karte hai to humko fields ko define karna padega uska model ko manually 
    password = serializers.CharField(max_length = 255, style = {'input_type':'password'}, write_only = True)

    password2 = serializers.CharField(max_length = 255, style = {'input_type':'password'}, write_only = True)

    class Meta:
        fields = ['passsword', 'password2']
    
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        # view me se jo context ke sath request.user send kar rahe hai to use yaha use karne ke liye self.context.get('user) ka use karte hai
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("password and confirm password doesn't match ")
        user.set_password(password)
        user.save()
        return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        print(attrs)
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email = email)
            print(user)
            # encode karenge user id ko or 
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token', token)
            link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
            print('Password Reset Link', link)
        #  Send EMail
            body = 'Click Following Link to Reset Your Password '+link
            data = {
            'subject':'Reset Your Password',
            'body':body,
            'to_email':user.email
                }
            # Util.send_email(data) 
           
                       
            return attrs
        else:
            raise serializers.ValidationError('You are not a Registered User')

class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      password2 = attrs.get('password2')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
    # decode encoded id and convert into string
      id = smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is Expired try again ')
      user.set_password(password)
      user.save()
      return attrs
    #   catch ke jagha except hota 
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')


