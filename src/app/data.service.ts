import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { catchError, Observable, throwError } from 'rxjs';

export interface BatterStats {
  // Define the structure of batter statistics based on pybaseball output
  name: any;
  season: number;
  Age: string;
  Team: string;
  Height: any;
  Weight: any;
  Bats: any;
  Throws: any;
  OPS: number;
  SLG: number;
  OBP: number;
  AVG: number;
  AB: number;
  H: number;
  doubles: number;
  triples: number;
  HR: number;
  R: number;
  RBI: number;
  SB: number;
  SO: number;
  IBB: number;
  HBP: number;
  SF: number;
  SH: number;
  GIDP: number;
}

export interface PitcherStats {
  // Define the structure of pitcher statistics based on pybaseball output
  name: any;
  season: number;
  age: string;
  team: string;
  height: any;
  weight: any;
  throws: any;
  W: number;
  L: number;
  SV: number;
  ERA: number;
  ER: number;
  SO: number;
  G: number;
  GS: number;
  CG: number;
  SHO: number;
  IPouts: number;
  H: number;
  HR: number;
  BB: number;
  BAOpp: number;
  WP: number;
  IBB: number;
  HBP: number;
  BK: number;
  BFP: number;
  GF: number;
  R: number;
  SH: number;
  SF: number;
  GIDP: number;
}

@Injectable({ providedIn: 'root' })
export class DataService {
  constructor(private http: HttpClient) { }

  getBatterStats(season: number): Observable<BatterStats[]> {
    const apiUrl = `http://127.0.0.1:5000/api/bat_stats/${season}`; 
    return this.http.get<BatterStats[]>(apiUrl)
      .pipe(
        catchError((error: HttpErrorResponse) => {
          console.error('HTTP Error:', error);
          return throwError(() => new Error('Failed to fetch batter stats.'));
        })
      );
  }

  getPitcherStats(season: number): Observable<PitcherStats[]> {
    const apiUrl = `http://127.0.0.1:5000/api/pitch_stats/${season}`; 
    return this.http.get<PitcherStats[]>(apiUrl)
      .pipe(
        catchError((error: HttpErrorResponse) => {
          console.error('HTTP Error:', error);
          return throwError(() => new Error('Failed to fetch pitcher stats.'));
        })
      );
  }
}