import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { EpisodeService } from '../../services/episode.service';
import { Episode } from '../../interfaces/models';

@Component({
  selector: 'app-episodes',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './episodes.component.html',
  styleUrl: './episodes.component.css'
})
export class EpisodesComponent implements OnInit {
  episodes: Episode[] = [];
  seasonNumber: number = 1;
  isLoading = false;
  errorMessage = '';

  constructor(
    private episodeService: EpisodeService,
    private route: ActivatedRoute,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.seasonNumber = Number(this.route.snapshot.paramMap.get('id'));
    this.loadEpisodes();
  }

  loadEpisodes() {
    this.isLoading = true;
    this.episodeService.getEpisodesBySeason(this.seasonNumber).subscribe({
      next: (data) => {
        this.episodes = [...data];
        this.isLoading = false;
        this.cdr.detectChanges();
      },
      error: () => {
        this.errorMessage = 'Failed to load episodes.';
        this.isLoading = false;
        this.cdr.detectChanges();
      }
    });
  }

  goBack() {
    this.router.navigate(['/seasons']);
  }
}