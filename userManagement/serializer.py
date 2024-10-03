from rest_framework import serializers
from userManagement.models import user, UserRoles
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, min_length=8, write_only=True)
    # roles = userRolesSerializer(many=True)
    #roles = serializers.PrimaryKeyRelatedField(queryset=UserRoles.objects.all(), required=True)

    class Meta:
        model = user
        fields = ['email', 'username', 'password','empId']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError('Username should not contain alpha numeric characters')

        return attrs

    def create(self, validated_data):
        return user.objects.create_user(**validated_data)


class loginSerializer(serializers.ModelSerializer):
    # email=serializers.EmailField(max_length=255, min_length=5)
    # tokens=serializers.SerializerMethodField()
    password=serializers.CharField(max_length=255, write_only=True)
    username=serializers.CharField(max_length=255)
    # email=serializers.EmailField(max_length=50, read_only=True)

    # def get_tokens(self, obj):
    #     users = user.objects.get(username=obj.get('username', ''))

    #     return {
    #         'access_token': users.tokens()['access_token'],
    #         'refresh_token': users.tokens()['refresh_token']
    #     }

    class Meta:
        model=user
        fields=['username','password', 'tokens']

    def validate(self, obj):
        name=obj.get('username', '')
        passWord=obj.get('password', '')

        # user = authenticate(request=self.context.get('request'), username=name, password=passWord)
        user = authenticate(username=name, password=passWord, is_active=True)

        if not user:
            raise AuthenticationFailed('Invalid Credentials')

        if not user.is_active:
            raise AuthenticationFailed('Account not valid, Contact admin')

        # if not user.is_email_verified:
        #     raise AuthenticationFailed('Email not verified')

        return {
            'email': user.email,
            'username': user.username,
            'id': user.id,
            'tokens': user.tokens()
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = "__all__"
