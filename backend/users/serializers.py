from django.contrib.auth import get_user_model
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, OpenApiTypes

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            "id", "username", "email", "first_name", "last_name",
            "display_name", "role", "promoter_type", "is_promoter_approved",
            "city", "country", "bio", "avatar",
        )
        read_only_fields = ("username", "role", "is_promoter_approved")

class UserUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False, allow_null=True)
    remove_avatar = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = User
        fields = (
            "first_name", "last_name", "email", "display_name",
            "bio", "avatar", "remove_avatar", "city", "country", "promoter_type",
        )

    def update(self, instance, validated_data):
        remove = validated_data.pop("remove_avatar", False)
        instance = super().update(instance, validated_data)
        if remove and instance.avatar:
            instance.avatar.delete(save=False)
            instance.avatar = None
            instance.save(update_fields=["avatar"])
        return instance

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    token = serializers.SerializerMethodField(required=False)  # optional

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "token")

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
        )

    @extend_schema_field(OpenApiTypes.STR)
    def get_token(self, obj):
        return ""  # optionally return a JWT if you add it later

class GoogleAuthSerializer(serializers.Serializer):
    id_token = serializers.CharField()