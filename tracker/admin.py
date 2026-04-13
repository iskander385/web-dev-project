from django.contrib import admin
from .models import UserProfile, Episode, CastMember, WatchLog, Review


# ─── Inline Admin ─────────────────────────────────────────────
# lets me add cast names from the episode page directly
class CastMemberInline(admin.TabularInline):
    model = CastMember
    extra = 3  # shows 3 empty cast slots by default


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ['user', 'rating', 'body', 'created_at']


# ─── Model Admin Classes ───────────────────────────────────────
@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['str', 'season_number', 'episode_number', 'air_date', 'imdb_rating']
    list_filter = ['season_number']
    search_fields = ['title', 'summary']
    inlines = [CastMemberInline, ReviewInline]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'joined_date']
    search_fields = ['user__username']


@admin.register(CastMember)
class CastMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'character_name', 'role_type', 'episode']
    list_filter = ['role_type']
    search_fields = ['name', 'character_name']


@admin.register(WatchLog)
class WatchLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'episode', 'watched_on', 'is_rewatch']
    list_filter = ['is_rewatch']
    search_fields = ['user__username']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'episode', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['user__username', 'body']