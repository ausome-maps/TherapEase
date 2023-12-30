from djoser.conf import settings
from djoser.serializers import TokenCreateSerializer
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers
from apps.core.facilities.serializers import FacilitiesSerializer
from .models import Profile, Organization


class UsersSerializer(serializers.ModelSerializer):
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
    user = UsersSerializer()

    class Meta:
        model = Profile
        exclude = ["login_count", "account_expiry"]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        user = instance.user
        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        instance.other_metadata = validated_data.get(
            "other_metadata", instance.other_metadata
        )
        user.save()
        instance.save()
        return super().update(instance, validated_data)


class OrganizationSerializer(serializers.ModelSerializer):
    members = UsersSerializer(read_only=True, many=True)
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
