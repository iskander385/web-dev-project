import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { WatchLog } from '../interfaces/models';

@Injectable({
  providedIn: 'root'
})
export class WatchLogService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getWatchLog(): Observable<WatchLog[]> {
    return this.http.get<WatchLog[]>(`${this.apiUrl}/watchlog/`);
  }

  markWatched(episodeId: number, isRewatch: boolean = false): Observable<WatchLog> {
    return this.http.post<WatchLog>(`${this.apiUrl}/watchlog/`, {
      episode: episodeId,
      is_rewatch: isRewatch
    });
  }

  removeFromWatchLog(episodeId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/watchlog/${episodeId}/`);
  }
}