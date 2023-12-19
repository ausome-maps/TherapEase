from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Profile


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    organization = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "password2",
            "email",
            "first_name",
            "last_name",
            "organization",
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
        profile.organization = validated_data["organization"]
        profile.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    organization = serializers.SerializerMethodField(method_name="get_organization")
    login_count = serializers.SerializerMethodField(method_name="get_login_count")
    account_expiry = serializers.SerializerMethodField(method_name="get_account_expiry")
    active = serializers.BooleanField(source="is_active")

    def get_organization(self, obj):
        return self.context["request"].user.profile.organization

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
            "organization",
            "login_count",
            "account_expiry",
        ]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        exclude = ["organization", "login_count", "account_expiry"]
