from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from exceptions import InvalidArgumentException
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth import get_user_model
User = get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True,)
    last_name = serializers.CharField(required=True,)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    date_of_birth = serializers.DateField(required=True)  # Add date_of_birth field

    class Meta:
        model = User
        fields = ('password', 'password2', 'email', 'first_name', 'last_name', 'date_of_birth')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise InvalidArgumentException({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            date_of_birth=validated_data['date_of_birth'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

# IF YOU WANT TO UPDATE RETURN OF TOKENS
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # data.update({
        # })
        return data