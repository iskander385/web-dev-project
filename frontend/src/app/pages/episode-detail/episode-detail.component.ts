import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { EpisodeService } from '../../services/episode.service';
import { ReviewService } from '../../services/review.service';
import { WatchLogService } from '../../services/watchlog.service';
import { AuthService } from '../../services/auth.service';
import { Episode, Review } from '../../interfaces/models';

@Component({
  selector: 'app-episode-detail',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './episode-detail.component.html',
  styleUrl: './episode-detail.component.css'
})
export class EpisodeDetailComponent implements OnInit {
  episode: Episode | null = null;
  reviews: Review[] = [];
  isLoggedIn = false;
  isWatched = false;
  isLoading = false;
  errorMessage = '';
  successMessage = '';

  reviewRating = 5;
  reviewBody = '';
  reviewError = '';
  reviewSuccess = '';
  submittingReview = false;

  editingReviewId: number | null = null;
  editRating = 5;
  editBody = '';

  currentUsername: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private episodeService: EpisodeService,
    private reviewService: ReviewService,
    private watchLogService: WatchLogService,
    private authService: AuthService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.route.paramMap.subscribe(params => {
      const id = Number(params.get('id'));
      this.isLoading = true;
      this.episode = null;
      this.reviews = [];
      this.currentUsername = this.authService.getUsername();
      this.authService.isLoggedIn$.subscribe(status => {
        this.isLoggedIn = status;
      });
      this.loadEpisode(id);
      this.loadReviews(id);
    });
  }

  loadEpisode(id: number) {
    this.episodeService.getEpisodeDetail(id).subscribe({
      next: (data) => {
        this.episode = data;
        this.isLoading = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.errorMessage = 'Failed to load episode.';
        this.isLoading = false;
        this.cdr.detectChanges();
      }
    });
  }

  loadReviews(id: number) {
    this.reviewService.getReviews(id).subscribe({
      next: (data) => {
        this.reviews = [...data];
        this.cdr.detectChanges();
      },
      error: () => this.reviewError = 'Failed to load reviews.'
    });
  }

  onMarkWatched() {
    if (!this.episode) return;
    this.watchLogService.markWatched(this.episode.id).subscribe({
      next: () => {
        this.isWatched = true;
        this.successMessage = 'Episode marked as watched!';
        this.cdr.detectChanges();
      },
      error: () => this.errorMessage = 'Failed to mark as watched.'
    });
  }

  onSubmitReview() {
    if (!this.episode) return;
    this.submittingReview = true;
    this.reviewError = '';
    this.reviewService.createReview(this.episode.id, {
      rating: this.reviewRating,
      body: this.reviewBody
    }).subscribe({
      next: (review) => {
        this.reviews.unshift(review);
        this.reviewBody = '';
        this.reviewRating = 5;
        this.reviewSuccess = 'Review submitted!';
        this.submittingReview = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.reviewError = err.error?.error || 'Failed to submit review.';
        this.submittingReview = false;
      }
    });
  }

  onDeleteReview(reviewId: number) {
    this.reviewService.deleteReview(reviewId).subscribe({
      next: () => {
        this.reviews = this.reviews.filter(r => r.id !== reviewId);
        this.cdr.detectChanges();
      },
      error: () => this.reviewError = 'Failed to delete review.'
    });
  }

  startEditReview(review: Review) {
    this.editingReviewId = review.id;
    this.editRating = review.rating;
    this.editBody = review.body;
  }

  onUpdateReview(reviewId: number) {
    this.reviewService.updateReview(reviewId, {
      rating: this.editRating,
      body: this.editBody
    }).subscribe({
      next: (updated) => {
        const index = this.reviews.findIndex(r => r.id === reviewId);
        if (index !== -1) this.reviews[index] = updated;
        this.editingReviewId = null;
        this.cdr.detectChanges();
      },
      error: () => this.reviewError = 'Failed to update review.'
    });
  }

  cancelEdit() {
    this.editingReviewId = null;
  }

  goBack() {
    if (this.episode) {
      this.router.navigate(['/seasons', this.episode.season_number, 'episodes']);
    }
  }

  getStars(rating: number): string {
    return '★'.repeat(rating) + '☆'.repeat(5 - rating);
  }
}