from django.urls import path
from . import views

urlpatterns = [
    # ─── Auth Endpoints ───────────────────────────────────────
    path('auth/register/', views.register_view, name='register'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),

    # ─── Episode Endpoints ────────────────────────────────────
    path('episodes/<int:pk>/', views.EpisodeDetailView.as_view(), name='episode-detail'),
    path('episodes/season/<int:season_number>/', views.episode_by_season_view, name='episodes-by-season'),

    # ─── Review Endpoints ─────────────────────────────────────
    path('episodes/<int:episode_id>/reviews/', views.ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),

    # ─── WatchLog Endpoints ───────────────────────────────────
    path('watchlog/', views.WatchLogView.as_view(), name='watchlog'),
    path('watchlog/<int:episode_id>/', views.WatchLogView.as_view(), name='watchlog-delete'),

    # ─── Profile Endpoints ────────────────────────────────────
    path('profile/', views.UserProfileView.as_view(), name='profile'),
]