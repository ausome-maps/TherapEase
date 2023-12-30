from djoser.conf import settings
from djoser.serializers import TokenCreateSerializer
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from apps.core.facilities.serializers import FacilitiesSerializer
from .models import Profile, Organization


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "password2",
            "email",
            "first_name",
            "last_name",
        ]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        user.set_password(validated_data["password"])
        user.save()
        profile = Profile.objects.get(user=user)
        profile.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    login_count = serializers.SerializerMethodField(method_name="get_login_count")
    account_expiry = serializers.SerializerMethodField(method_name="get_account_expiry")
    active = serializers.BooleanField(source="is_active")

    def get_login_count(self, obj):
        return self.context["request"].user.profile.login_count

    def get_account_expiry(self, obj):
        return self.context["request"].user.profile.account_expiry

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "active",
            "login_count",
            "account_expiry",
        ]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        exclude = ["login_count", "account_expiry"]


class OrganizationSerializer(serializers.ModelSerializer):
    members = UserSerializer(read_only=True, many=True)
    facilities = FacilitiesSerializer(read_only=True, many=True)

    class Meta:
        model = Organization
        fields = "__all__"


class CustomTokenCreateSerializer(TokenCreateSerializer):
    def validate(self, attrs):
        password = attrs.get("password")
        params = {settings.LOGIN_FIELD: attrs.get(settings.LOGIN_FIELD)}
        self.user = authenticate(
            request=self.context.get("request"), **params, password=password
        )
        if not self.user:
            User = get_user_model()
            self.user = User.objects.filter(**params).first()
            if self.user and not self.user.check_password(password):
                self.fail("invalid_credentials")
        # We changed only below line
        if self.user:  # and self.user.is_active:
            return attrs
        self.fail("invalid_credentials")
