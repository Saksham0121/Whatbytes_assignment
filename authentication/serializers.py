"""
Serializers for user registration and login.

All user inputs are validated and sanitized before processing.
Passwords are hashed using Django's built-in PBKDF2 hasher.
"""

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from healthcare_backend.sanitizer import sanitize


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Validates email uniqueness, password strength, and sanitizes text inputs.
    """

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        validators=[validate_password],
        style={"input_type": "password"},
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "password", "password_confirm")
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "email": {"required": True},
        }

    def validate_email(self, value):
        """Ensure email is unique and sanitized."""
        email = sanitize(value).lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return email

    def validate_first_name(self, value):
        """Sanitize first name input."""
        return sanitize(value)

    def validate_last_name(self, value):
        """Sanitize last name input."""
        return sanitize(value)

    def validate(self, attrs):
        """Ensure both passwords match."""
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "Passwords do not match."}
            )
        return attrs

    def create(self, validated_data):
        """Create user with hashed password."""
        validated_data.pop("password_confirm")
        user = User.objects.create_user(
            username=validated_data["email"],  # Use email as username
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            password=validated_data["password"],
        )
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    Validates credentials and returns user object on success.
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={"input_type": "password"},
    )

    def validate(self, attrs):
        email = sanitize(attrs["email"]).lower()
        password = attrs["password"]

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                "Invalid email or password. Please try again."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "This account has been deactivated."
            )

        attrs["user"] = user
        return attrs
