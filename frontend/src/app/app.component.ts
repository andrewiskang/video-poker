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

  constructor(private gameService: GameService) {}

  ngOnInit() {

  }

  drawCards() {
    var payload = {
      denomination: this.denomination,
      numCredits: this.numCredits
    }
    this.gameService.drawCards(this.gameId, payload).subscribe(data => {
      data.hand.forEach(card => {
        card.held = false
      })
      this.hand = data.hand
      this.bankroll = data.bankroll
      this.outcome = data.outcome
    })
  }

  // redrawCards() {
  //   var payload = {
  //     holdIndices: 
  //   }
  // }
}

