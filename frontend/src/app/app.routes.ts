import { Routes } from '@angular/router';
import { authGuard } from './guards/auth.guard';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./pages/home/home.component').then(m => m.HomeComponent)
  },

  {
    path: 'login',
    loadComponent: () => import('./pages/login/login.component').then(m => m.LoginComponent)
  },
  {
    path: 'register',
    loadComponent: () => import('./pages/register/register.component').then(m => m.RegisterComponent)
  },

  {
    path: 'seasons',
    loadComponent: () => import('./pages/seasons/seasons.component').then(m => m.SeasonsComponent)
  },
  {
    path: 'seasons/:id/episodes',
    loadComponent: () => import('./pages/episodes/episodes.component').then(m => m.EpisodesComponent)
  },
  {
    path: 'episodes/:id',
    loadComponent: () => import('./pages/episode-detail/episode-detail.component').then(m => m.EpisodeDetailComponent)
  },

  {
    path: 'profile',
    loadComponent: () => import('./pages/profile/profile.component').then(m => m.ProfileComponent),
    canActivate: [authGuard]
  },
  {
    path: 'profile/:username',
    loadComponent: () => import('./pages/profile/profile.component').then(m => m.ProfileComponent)
  },

  {
    path: '**',
    redirectTo: 'seasons'
  }
];