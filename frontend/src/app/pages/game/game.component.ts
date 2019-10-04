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
  bankroll: number
  outcome: string
  payout: any
  creditsWon: number
  inPlay: boolean
  holdIndices: boolean[]

  constructor(private gameService: GameService, private authService: AuthService) { }

  ngOnInit() {
    this.authService.user.subscribe(user => {
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
          this.holdIndices = [false, false, false, false, false]
        }
      })
    })
  }

  startNewGame() {
    this.gameService.startNewGame(this.userId, {}).subscribe(data => {
      console.log('new game started ' + data.update_time)
      this.updateGame(data.game)
    })
  }

  drawCards() {
    var payload = {
      denomination: this.denomination,
      numCredits: this.numCredits
    }
    this.gameService.drawCards(this.userId, payload).subscribe(game => {
      this.updateGame(game)
      this.holdIndices = [false, false, false, false, false]
    })
  }

  redrawCards() {
    var payload = { holdIndices: this.holdIndices }
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

