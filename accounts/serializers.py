from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Signup/Register Serializer
    """
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    confirm_password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate(self, data):
        """
        Check validation of password
        """
        password = data.get("password")
        confirm_password = data.pop("confirm_password")
        if password and confirm_password and password == confirm_password:
            return data
        raise serializers.ValidationError("Password doesn't match")
