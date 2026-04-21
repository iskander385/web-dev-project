import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Review } from '../interfaces/models';

@Injectable({
  providedIn: 'root'
})
export class ReviewService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getReviews(episodeId: number): Observable<Review[]> {
    return this.http.get<Review[]>(`${this.apiUrl}/episodes/${episodeId}/reviews/`);
  }

  createReview(episodeId: number, data: { rating: number; body: string }): Observable<Review> {
    return this.http.post<Review>(`${this.apiUrl}/episodes/${episodeId}/reviews/`, data);
  }

  updateReview(reviewId: number, data: { rating: number; body: string }): Observable<Review> {
    return this.http.put<Review>(`${this.apiUrl}/reviews/${reviewId}/`, data);
  }

  deleteReview(reviewId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/reviews/${reviewId}/`);
  }
}