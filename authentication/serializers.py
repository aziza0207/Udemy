from rest_framework import serializers
from authentication.models import User


class RegisterSerializer(serializers.ModelSerializer):
    is_mentor = serializers.BooleanField(default=False)
    finished_registration = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        finished_registration = True
        if validated_data["is_mentor"]:
            finished_registration = False

        user = User.objects.create_user(
            full_name=validated_data["full_name"],
            email=validated_data["email"],
            is_mentor=validated_data["is_mentor"],
            password=validated_data["password"],
            finished_registration=finished_registration,
            username=validated_data["email"],
        )
        return user

    class Meta:
        model = User
        fields = [
            "id",
            'full_name',
            'email',
            'password',
            'is_mentor',
            'finished_registration',

        ]


class MentorRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "audition",
            "type_of_teaching",
        ]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField()
    password2 = serializers.CharField()
