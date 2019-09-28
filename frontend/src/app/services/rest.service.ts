import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RestService {

  protected baseUrl: string = 'http://localhost:5000/api'

  constructor(private http: HttpClient) { }

  protected get(relativeUrl: string, responseType: any = 'json'): Observable<any> {
    return this.http.get(this.baseUrl + relativeUrl, { responseType: responseType })
  }

  protected post(relativeUrl: string, data: any, responseType: any = 'json'): Observable<any> {
    return this.http.post(this.baseUrl + relativeUrl, data, { responseType: responseType })
  }

  protected put(relativeUrl: string, data: any, responseType: any = 'json'): Observable<any> {
    return this.http.put(this.baseUrl + relativeUrl, data, { responseType: responseType })
  }
}
