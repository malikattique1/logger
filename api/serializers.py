
from rest_framework import serializers
from core.models import Illusion, UserResponse
from django.contrib.auth.models import User
# from rest_framework.response import Response


class IllusionSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False)
    portrait_link = serializers.URLField(required=False)
    landscape_link = serializers.URLField(required=False)
    portrait_solution_link = serializers.URLField(required=False)
    landscape_solution_link = serializers.URLField(required=False)
    answer_quad_points = serializers.CharField(required=False)
    points = serializers.CharField(required=False)
    difficulty_level = serializers.CharField(required=False)
    status = serializers.CharField(required=False)

    class Meta:
        model = Illusion
        fields = [
            'id',
            'title',
            'portrait_link',
            'landscape_link',
            'portrait_solution_link',
            'landscape_solution_link',
            'answer_quad_points',
            'points',
            'difficulty_level',
            'status',
            'created_at',
            'updated_at'
        ]

    def create(self, validated_data):
        return Illusion.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.portrait_link = validated_data.get('portrait_link', instance.portrait_link)
        instance.landscape_link = validated_data.get('landscape_link', instance.landscape_link)
        instance.portrait_solution_link = validated_data.get('portrait_solution_link', instance.portrait_solution_link)
        instance.landscape_solution_link = validated_data.get('landscape_solution_link', instance.landscape_solution_link)
        instance.answer_quad_points = validated_data.get('answer_quad_points', instance.answer_quad_points)
        instance.points = validated_data.get('points', instance.points)
        instance.difficulty_level = validated_data.get('difficulty_level', instance.difficulty_level)
        instance.status = validated_data.get('status', instance.status)

        instance.save()
        return instance


class UserResponseSerializer(serializers.ModelSerializer):
    userid = serializers.CharField(required=False)
    # illusion-id = serializers.URLField(required=False)

    class Meta:
        model = UserResponse
        fields = [
            'id',
            'userid',
            'illusion-id',
            'success',
            'created_at',
            'updated_at'
        ]

    def create(self, validated_data):
        return Illusion.objects.create(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    is_active = serializers.BooleanField(required=False)
    # is_staff = serializers.BooleanField(required=False)
    # is_superuser = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = [
            'id',
            'password',
            'username',
            'first_name',
            'last_name',
            'is_active',
            # 'is_superuser',
            # 'is_staff'
        ]

    def create(self, validated_data):
        return User.objects.create(**validated_data)


