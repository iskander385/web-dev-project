export interface User {
  id: number;
  username: string;
  email: string;
}

export interface UserProfile {
  id: number;
  username: string;
  email: string;
  bio: string;
  avatar: string;
  joined_date: string;
}

export interface CastMember {
  id: number;
  name: string;
  character_name: string;
  role_type: 'main' | 'guest' | 'recurring';
}

export interface Episode {
  id: number;
  season_number: number;
  episode_number: number;
  title: string;
  summary: string;
  air_date: string;
  runtime: number;
  imdb_rating: number;
  poster_url: string;
  cast: CastMember[];
}

export interface Review {
  id: number;
  username: string;
  episode: number;
  episode_title: string;
  season_number: number;
  episode_number: number;
  rating: number;
  body: string;
  created_at: string;
  updated_at: string;
}

export interface WatchLog {
  id: number;
  episode: number;
  episode_title: string;
  season_number: number;
  episode_number: number;
  poster_url: string;
  watched_on: string;
  is_rewatch: boolean;
}

export interface AuthResponse {
  message: string;
  tokens: {
    access: string;
    refresh: string;
  };
  username: string;
}

export interface ProfileResponse {
  profile: UserProfile;
  stats: {
    total_watched: number;
    total_reviews: number;
    watched_by_season: { [key: number]: number };
  };
  recent_reviews: Review[];
}