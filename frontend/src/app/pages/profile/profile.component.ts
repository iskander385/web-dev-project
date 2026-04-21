import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ProfileService } from '../../services/profile.service';
import { AuthService } from '../../services/auth.service';
import { ProfileResponse } from '../../interfaces/models';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.css'
})
export class ProfileComponent implements OnInit {
  profileData: ProfileResponse | null = null;
  isOwnProfile = false;
  isLoading = false;
  errorMessage = '';
  editingBio = false;
  newBio = '';

  constructor(
    private profileService: ProfileService,
    private authService: AuthService,
    private route: ActivatedRoute,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.route.paramMap.subscribe(params => {
      const username = params.get('username');
      const currentUsername = this.authService.getUsername();

      if (username) {
        this.isOwnProfile = username === currentUsername;
        this.loadPublicProfile(username);
      } else {
        this.isOwnProfile = true;
        this.loadMyProfile();
      }
    });
  }

  loadMyProfile() {
    this.isLoading = true;
    this.profileService.getMyProfile().subscribe({
      next: (data) => {
        this.profileData = data;
        this.newBio = data.profile.bio;
        this.isLoading = false;
        this.cdr.detectChanges();
      },
      error: () => {
        this.errorMessage = 'Failed to load profile.';
        this.isLoading = false;
        this.cdr.detectChanges();
      }
    });
  }

  loadPublicProfile(username: string) {
    this.isLoading = true;
    this.profileService.getPublicProfile(username).subscribe({
      next: (data) => {
        this.profileData = data;
        this.isLoading = false;
        this.cdr.detectChanges();
      },
      error: () => {
        this.errorMessage = 'User not found.';
        this.isLoading = false;
        this.cdr.detectChanges();
      }
    });
  }

  onUpdateBio() {
    this.profileService.updateProfile({ bio: this.newBio }).subscribe({
      next: () => {
        if (this.profileData) {
          this.profileData.profile.bio = this.newBio;
        }
        this.editingBio = false;
        this.cdr.detectChanges();
      },
      error: () => this.errorMessage = 'Failed to update bio.'
    });
  }

  getSeasonNumbers(): number[] {
    if (!this.profileData?.stats.watched_by_season) return [];
    return Object.keys(this.profileData.stats.watched_by_season).map(Number).sort((a, b) => a - b);
  }

  goToSeasons() {
    this.router.navigate(['/seasons']);
  }
}