import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class CurrencyService {
  private API_URL = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  getCurrenciesByDate(date: string): Observable<any> {
    return this.http.get(`${this.API_URL}/currencies/${date}`);
  }

  fetchFromBackend(): Observable<any> {
    return this.http.post(`${this.API_URL}/currencies/fetch`, {});
  }

  getAllCurrencies(): Observable<any> {
    return this.http.get(`${this.API_URL}/currencies`);
  }
}
