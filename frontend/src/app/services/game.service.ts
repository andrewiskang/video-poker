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

  drawCards(gameId: string, payload: object) {
    return this.post('/games/' + gameId + '/draw', payload)
  }

  redrawCards(gameId: string, payload: object) {
    return this.post('/games/' + gameId + '/redraw', payload)
  }

}
