import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service'
import { Router } from '@angular/router'

import { faGoogle, faFacebookSquare } from '@fortawesome/free-brands-svg-icons';
import { faEnvelope, faPhoneAlt  } from '@fortawesome/free-solid-svg-icons';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  faGoogle = faGoogle
  faFacebookSquare = faFacebookSquare
  faEnvelope = faEnvelope
  faPhoneAlt = faPhoneAlt

  constructor(private authService: AuthService, private router: Router) { }

  ngOnInit() {
    this.authService.user.subscribe(user => {
      if (user) {
        console.log('already logged in')
        this.router.navigateByUrl('/')
      }
    })
  }

  googleLogin() {
    this.authService.googleLogin()
  }
}
