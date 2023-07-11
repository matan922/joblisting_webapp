from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from main_joblist_app.models import CustomUser
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework import serializers
from rest_framework.serializers import ValidationError



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username

        return token


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required = True, validators=[UniqueValidator(queryset=CustomUser.objects.all(), message={"error": "Email already exists."})])
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
        
    class Meta:
        model = CustomUser
        fields = '__all__'

        
    def validate(self, pwd):
        """
        check if passwords match.
        """
        if pwd['password'] != pwd['password2']:
            raise ValidationError({"error":"Passwords must match!"})
        return pwd
        
    def create(self, validated_data):
        
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )

        # user = CustomUser(
        #     email=validated_data['email'],
        #     username=validated_data['username'],
        #     first_name=validated_data['first_name'],
        #     last_name=validated_data['last_name'],
        # )
        
        # user.set_password(validated_data['password'])
        # user.save()
                
        return user


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    
    
    def validate(self,attrs):
        # Saving the user's refresh token in a variable
        self.token = attrs['refresh']
        return attrs
    
    
    def save(self,**kwargs):
        try:
            # Blacklisting the refresh token
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise ValidationError('Expired or invalid refresh token')