import { Component, OnInit } from '@angular/core';
import { GameService } from './services/game.service'

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

  hand: any[]
  denomination: number = 1
  numCredits: number = 5
  gameId: string = 'LXgAEAK2IbTUP59KtBuR'
  bankroll: number
  outcome: string
  payout: any
  creditsWon: number
  inPlay: boolean = false
  holdIndices = [false, false, false, false, false]

  constructor(private gameService: GameService) { }

  ngOnInit() {

  }

  drawCards() {
    var payload = {
      denomination: this.denomination,
      numCredits: this.numCredits
    }
    this.gameService.drawCards(this.gameId, payload).subscribe(data => {
      this.hand = data.hand
      this.bankroll = data.bankroll
      this.outcome = data.outcome
      this.creditsWon = 0
      this.inPlay = true
      this.holdIndices = [false, false, false, false, false]
    })
  }

  redrawCards() {
    var payload = { holdIndices: this.holdIndices }
    this.gameService.redrawCards(this.gameId, payload).subscribe(data => {
      this.hand = data.hand
      this.bankroll = data.bankroll
      this.outcome = data.outcome
      this.creditsWon = data.creditsWon
      this.inPlay = false
    })
  }

  // redrawCards() {
  //   var payload = {
  //     holdIndices: 
  //   }
  // }
}

