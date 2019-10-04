import { Component, OnInit } from '@angular/core';
import { AuthService } from './services/auth.service'

import { faCaretDown, faBars } from '@fortawesome/free-solid-svg-icons'

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

  user: any = 'null';
  faCaretDown = faCaretDown;
  faBars = faBars;

  constructor(private authService: AuthService) { }

  ngOnInit() {
    this.authService.user.subscribe(user => {
      this.user = user
    })
  }

  signOut() {
    this.authService.signOut()
    this.user = null
  }
}

