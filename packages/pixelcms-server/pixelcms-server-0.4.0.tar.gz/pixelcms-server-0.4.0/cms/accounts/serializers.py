from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import (
    get_default_password_validators
)

from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class RegisterSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'[a-zA-Z0-9\-_]',
        min_length=3,
        max_length=30
    )
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)
    password2 = serializers.CharField(max_length=255)

    def validate_username(self, val):
        user = get_user_model().objects.filter(username=val).exists()
        if user:
            raise serializers.ValidationError(
                _('Provided username is already taken.')
            )
        return val

    def validate_email(self, val):
        user = get_user_model().objects.filter(email=val).exists()
        if user:
            raise serializers.ValidationError(
                _('Provided email address is already taken.')
            )
        return val

    def validate_password(self, val):
        validators = get_default_password_validators()
        for v in validators:
            v.validate(val)
        return val

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(_('Passwords do not match.'))
        return data


class ActivateSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=255)


class ResendActivationMessageSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)


class SendResetPasswordMessageSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)


class ResetPasswordSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    password2 = serializers.CharField(max_length=255)

    def validate_password(self, val):
        validators = get_default_password_validators()
        for v in validators:
            v.validate(val)
        return val

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(_('Passwords do not match.'))
        return data


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=255)
    new_password = serializers.CharField(max_length=255)
    new_password2 = serializers.CharField(max_length=255)

    def validate_current_password(self, val):
        user = authenticate(
            username=self.context['request'].user.username,
            password=val
        )
        if not user:
            raise serializers.ValidationError(
                _('Current password is invalid.')
            )
        return val

    def validate_new_password(self, val):
        validators = get_default_password_validators()
        for v in validators:
            v.validate(val)
        return val

    def validate(self, data):
        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError(_('Passwords do not match.'))
        return data


class ChangeEmailSerializer(serializers.Serializer):
    new_email = serializers.EmailField(max_length=255)

    def validate_new_email(self, val):
        user = get_user_model().objects.filter(email=val).exists()
        if user:
            raise serializers.ValidationError(
                _('Provided email address is already taken.')
            )
        return val


class ChangeEmailConfirmationSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=255)
