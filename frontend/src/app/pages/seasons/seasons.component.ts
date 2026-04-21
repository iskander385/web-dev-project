import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-seasons',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './seasons.component.html',
  styleUrl: './seasons.component.css'
})
export class SeasonsComponent implements OnInit {
  seasons = Array.from({ length: 15 }, (_, i) => ({
    number: i + 1,
    episodeCount: this.getEpisodeCount(i + 1)
  }));

  username: string | null = null;
  isLoggedIn = false;

  constructor(private authService: AuthService, private router: Router) {}

  ngOnInit() {
    this.username = this.authService.getUsername();
    this.authService.isLoggedIn$.subscribe(status => {
      this.isLoggedIn = status;
    });
  }

  getEpisodeCount(season: number): number {
    const counts: { [key: number]: number } = {
      1: 22, 2: 22, 3: 16, 4: 22, 5: 22,
      6: 22, 7: 23, 8: 23, 9: 23, 10: 23,
      11: 23, 12: 23, 13: 23, 14: 20, 15: 20
    };
    return counts[season] || 22;
  }

  onLogout() {
    this.authService.logout().subscribe({
      next: () => this.router.navigate(['/login']),
      error: () => {
        this.authService.clearTokens();
        this.router.navigate(['/login']);
      }
    });
  }
}