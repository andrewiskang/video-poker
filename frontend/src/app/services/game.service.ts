import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { RestService } from './rest.service';

@Injectable({
  providedIn: 'root'
})
export class GameService extends RestService {

  constructor(http: HttpClient) {
    super(http)
  }

  getGame(userId: string) {
    return this.get('/games/' + userId)
  }

  startNewGame(userId: string, payload: object) {
    return this.post('/games/' + userId, payload)
  }

  drawCards(userId: string, payload: object) {
    return this.post('/games/' + userId + '/draw', payload)
  }

  redrawCards(userId: string, payload: object) {
    return this.post('/games/' + userId + '/redraw', payload)
  }

}
