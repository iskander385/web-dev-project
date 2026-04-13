from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile, Episode, CastMember, WatchLog, Review


# ─── Base Serializers (serializers.Serializer) ─────────────────
# These satisfy the "at least 2 from serializers.Serializer" requirement

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    password_confirm = serializers.CharField(required=True, write_only=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # Automatically create a UserProfile when a new user registers
        UserProfile.objects.create(user=user)
        return user


# ─── Model Serializers (serializers.ModelSerializer) ───────────
# These satisfy the "at least 2 from serializers.ModelSerializer" requirement

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'bio', 'avatar', 'joined_date']


class CastMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CastMember
        fields = ['id', 'name', 'character_name', 'role_type']


class EpisodeSerializer(serializers.ModelSerializer):
    cast = CastMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Episode
        fields = [
            'id',
            'season_number',
            'episode_number',
            'title',
            'summary',
            'air_date',
            'runtime',
            'imdb_rating',
            'poster_url',
            'cast',
        ]


class WatchLogSerializer(serializers.ModelSerializer):
    # Show episode title in the response instead of just the ID
    episode_title = serializers.CharField(source='episode.title', read_only=True)
    season_number = serializers.IntegerField(source='episode.season_number', read_only=True)
    episode_number = serializers.IntegerField(source='episode.episode_number', read_only=True)

    class Meta:
        model = WatchLog
        fields = ['id', 'episode', 'episode_title', 'season_number', 'episode_number', 'watched_on', 'is_rewatch']
        read_only_fields = ['watched_on']

    def create(self, validated_data):
        # Automatically attach the logged in user
        user = self.context['request'].user
        return WatchLog.objects.create(user=user, **validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    # Show username in the response instead of just the user ID
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'username', 'episode', 'rating', 'body', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        # Automatically attach the logged in user
        user = self.context['request'].user
        return Review.objects.create(user=user, **validated_data)