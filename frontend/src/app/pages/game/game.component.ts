import { Component, OnInit } from '@angular/core';
import { GameService } from '../../services/game.service'
import { AuthService } from '../../services/auth.service'

@Component({
  selector: 'app-game',
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.css']
})
export class GameComponent implements OnInit {

  hand: any[] = [null, null, null, null, null]
  denomination: number
  numCredits: number
  userId: string
  bankroll: number = 0
  outcome: string
  payout: any
  creditsWon: number = 0
  inPlay: boolean

  constructor(private gameService: GameService, private authService: AuthService) { }

  ngOnInit() {
    this.authService.user.subscribe(user => {
      // console.log(user)
      if (user) {
        this.userId = user.uid
        this.gameService.getGame(this.userId).subscribe(game => {
          if (!game) {
            this.startNewGame()
          }
          else {
            if (!game.inPlay) {
              game.hand = [null, null, null, null, null]
              game.creditsWon = 0
              game.outcome = ''
            }
            this.updateGame(game)
          }
        })
      }
    })
  }

  startNewGame() {
    this.gameService.startNewGame(this.userId, {}).subscribe(data => {
      console.log('new game started ' + data.update_time)
      data.game.hand = [null, null, null, null, null]
      this.updateGame(data.game)
    })
  }

  drawCards() {
    this.hand = [null, null, null, null, null]
    var payload = {
      denomination: this.denomination,
      numCredits: this.numCredits
    }
    this.gameService.drawCards(this.userId, payload).subscribe(game => {
      this.updateGame(game)
    })
  }

  redrawCards() {
    var payload = { hand: [...this.hand] }
    for (let i = 0; i < this.hand.length; i++) {
      if (!this.hand[i].held) {
        this.hand[i] = null
      }
    }
    // console.log(payload)
    this.gameService.redrawCards(this.userId, payload).subscribe(game => {
      this.updateGame(game)
    })
  }

  updateGame(game) {
    this.denomination = game.denomination
    this.numCredits = game.numCredits
    this.bankroll = game.bankroll
    this.hand = game.hand
    this.payout = game.payout
    this.creditsWon = game.creditsWon
    this.outcome = game.outcome
    this.inPlay = game.inPlay
  }

}

