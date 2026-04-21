import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Episode } from '../interfaces/models';

@Injectable({
  providedIn: 'root'
})
export class EpisodeService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getEpisodesBySeason(seasonNumber: number): Observable<Episode[]> {
    return this.http.get<Episode[]>(`${this.apiUrl}/episodes/season/${seasonNumber}/`);
  }

  getEpisodeDetail(id: number): Observable<Episode> {
    return this.http.get<Episode>(`${this.apiUrl}/episodes/${id}/`);
  }
}