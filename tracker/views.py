from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Episode, WatchLog, Review, UserProfile
from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    EpisodeSerializer,
    WatchLogSerializer,
    ReviewSerializer,
    UserProfileSerializer,
)


#helper
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


#function based views (FBV)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response({
            'message': 'Account created successfully.',
            'tokens': tokens,
            'username': user.username,
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user is not None:
            tokens = get_tokens_for_user(user)
            return Response({
                'message': 'Login successful.',
                'tokens': tokens,
                'username': user.username,
            }, status=status.HTTP_200_OK)
        return Response(
            {'error': 'Invalid username or password.'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data['refresh']
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)
    except Exception:
        return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def episode_by_season_view(request, season_number):
    episodes = Episode.objects.by_season(season_number)
    if not episodes.exists():
        return Response(
            {'error': f'No episodes found for season {season_number}.'},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = EpisodeSerializer(episodes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


#class based views (CBV)

class EpisodeDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            episode = Episode.objects.get(pk=pk)
        except Episode.DoesNotExist:
            return Response(
                {'error': 'Episode not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = EpisodeSerializer(episode)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewListCreateView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get(self, request, episode_id):
        reviews = Review.objects.filter(episode_id=episode_id).order_by('-created_at')
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, episode_id):
        # Check if user already reviewed this episode
        if Review.objects.filter(user=request.user, episode_id=episode_id).exists():
            return Response(
                {'error': 'You have already reviewed this episode.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = request.data.copy()
        data['episode'] = episode_id
        serializer = ReviewSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Review.objects.get(pk=pk, user=user)
        except Review.DoesNotExist:
            return None

    def put(self, request, pk):
        review = self.get_object(pk, request.user)
        if not review:
            return Response(
                {'error': 'Review not found or not yours to edit.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ReviewSerializer(review, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        review = self.get_object(pk, request.user)
        if not review:
            return Response(
                {'error': 'Review not found or not yours to delete.'},
                status=status.HTTP_404_NOT_FOUND
            )
        review.delete()
        return Response({'message': 'Review deleted.'}, status=status.HTTP_204_NO_CONTENT)


class WatchLogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logs = WatchLog.objects.filter(user=request.user).order_by('-watched_on')
        serializer = WatchLogSerializer(logs, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = WatchLogSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, episode_id):
        try:
            log = WatchLog.objects.get(user=request.user, episode_id=episode_id)
            log.delete()
            return Response({'message': 'Watch log removed.'}, status=status.HTTP_204_NO_CONTENT)
        except WatchLog.DoesNotExist:
            return Response({'error': 'Log not found.'}, status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'Profile not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = UserProfileSerializer(profile)
        total_watched = WatchLog.objects.filter(user=request.user).count()
        total_reviews = Review.objects.filter(user=request.user).count()

        # group watched episodes by season for the progress bars in Angular
        watched_by_season = {}
        for log in WatchLog.objects.filter(user=request.user).select_related('episode'):
            season = log.episode.season_number
            watched_by_season[season] = watched_by_season.get(season, 0) + 1

        recent_reviews = Review.objects.filter(
            user=request.user
        ).order_by('-created_at')[:5]
        recent_serializer = ReviewSerializer(recent_reviews, many=True)

        return Response({
            'profile': serializer.data,
            'stats': {
                'total_watched': total_watched,
                'total_reviews': total_reviews,
                'watched_by_season': watched_by_season,
            },
            'recent_reviews': recent_serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'Profile not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PublicProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        profile = UserProfile.objects.get(user=user)
        serializer = UserProfileSerializer(profile)
        total_watched = WatchLog.objects.filter(user=user).count()
        total_reviews = Review.objects.filter(user=user).count()
        recent_reviews = Review.objects.filter(user=user).order_by('-created_at')[:5]
        recent_serializer = ReviewSerializer(recent_reviews, many=True)
        return Response({
            'profile': serializer.data,
            'stats': {
                'total_watched': total_watched,
                'total_reviews': total_reviews,
            },
            'recent_reviews': recent_serializer.data
        }, status=status.HTTP_200_OK)