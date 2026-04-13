from django.db import models
from django.contrib.auth.models import User


# ─── Custom Manager ───────────────────────────────────────────
class EpisodeManager(models.Manager):
    def by_season(self, season_number):
        return self.filter(season_number=season_number).order_by('episode_number')


# ─── Models ───────────────────────────────────────────────────
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    joined_date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.user.username}'s Profile"


class Episode(models.Model):
    season_number = models.IntegerField()
    episode_number = models.IntegerField()
    title = models.CharField(max_length=200)
    summary = models.TextField()
    air_date = models.DateField(null=True, blank=True)
    runtime = models.IntegerField(help_text="Runtime in minutes", null=True, blank=True)
    imdb_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    poster_url = models.URLField(blank=True)

    # Custom manager
    objects = EpisodeManager()

    class Meta:
        ordering = ['season_number', 'episode_number']
        unique_together = ['season_number', 'episode_number']

    def str(self):
        return f"S{self.season_number:02d}E{self.episode_number:02d} - {self.title}"


class CastMember(models.Model):
    ROLE_CHOICES = [
        ('main', 'Main Cast'),
        ('guest', 'Guest Star'),
        ('recurring', 'Recurring'),
    ]

    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='cast')
    name = models.CharField(max_length=200)
    character_name = models.CharField(max_length=200)
    role_type = models.CharField(max_length=20, choices=ROLE_CHOICES, default='guest')

    def str(self):
        return f"{self.name} as {self.character_name}"


class WatchLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlogs')
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='watchlogs')
    watched_on = models.DateField(auto_now_add=True)
    is_rewatch = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'episode']

    def str(self):
        return f"{self.user.username} watched {self.episode}"


class Review(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]  # 1 to 5 stars

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'episode']  # one review per episode per user

    def str(self):
        return f"{self.user.username} - {self.episode} ({self.rating}★)"