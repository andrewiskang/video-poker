import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  hand: any[] = [
      {
          rank: {
              name: 'seven',
              symbol: '7',
              value: 7
          },
          suit: {
              name: 'heart',
              symbol: '♥',
              color: 'red'
          }
      },
      {
          rank: {
              name: 'three',
              symbol: '3',
              value: 3
          },
          suit: {
              name: 'heart',
              symbol: '♥',
              color: 'red'
          }
      },
      {
          rank: {
              name: 'ace',
              symbol: 'A',
              value: 1
          },
          suit: {
              name: 'heart',
              symbol: '♥',
              color: 'red'
          }
      },
      {
          rank: {
              name: 'king',
              symbol: 'K',
              value: 13
          },
          suit: {
              name: 'heart',
              symbol: '♥',
              color: 'red'
          }
      },
      {
          rank: {
              name: 'ten',
              symbol: '10',
              value: 10
          },
          suit: {
              name: 'heart',
              symbol: '♥',
              color: 'red'
          }
      }
  ]
}

      //         symbol: '♣',
      //     color: 'black'
      //   },
      //   diamond: {
      //     name: 'diamond',
      //     symbol: '♦',
      //     color: 'red'
      //   },
      //   spade: {
      //     name: 'spade',
      //     symbol: '♠',
      //     color: 'black'
      //   },
      //   heart: {
      //     name: 'heart',
      //     symbol: '♥',
      //     color: 'red'
      //   }
      // };
