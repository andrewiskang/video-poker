import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { AngularFireAuth } from '@angular/fire/auth';
import { AngularFirestore, AngularFirestoreDocument } from '@angular/fire/firestore';
import { auth } from 'firebase/app';

import { Observable, of } from 'rxjs';
import { switchMap } from 'rxjs/operators';

interface User {
  uid: string
  email: string
  photoURL?: string
  displayName?: string
}


@Injectable({
  providedIn: 'root'
})
export class AuthService {

  user: Observable<User>

  constructor(private afAuth: AngularFireAuth, private afs: AngularFirestore, private router: Router) {
    //// Get auth data, then get firestore user document || null
    this.afAuth.auth.getRedirectResult()
      .then(credential => {
        if (credential.user) {
          this.updateUserData(credential.user)
        }
      })
      .catch(error => {
        console.log(error)
      })
    this.user = this.afAuth.authState.pipe(
      switchMap(user => {
        if (user) {
          return this.afs.doc<User>(`users/${user.uid}`).valueChanges()
        }
        else {
          return of(null)
        }
      })
    )
  }

  googleLogin() {
    const provider = new auth.GoogleAuthProvider()
    return this.oAuthLogin(provider)
  }

  facebookLogin() {
    var provider = new auth.FacebookAuthProvider()
    provider.addScope('email');
    return this.oAuthLogin(provider)
  }

  private oAuthLogin(provider) {
    return this.afAuth.auth.signInWithRedirect(provider)
  }

  private updateUserData(user) {
    // Sets user data to firestore on login
    const userRef: AngularFirestoreDocument<any> = this.afs.doc(`users/${user.uid}`)
    const data: User = {
      uid: user.uid,
      email: user.email,
      displayName: user.displayName,
      photoURL: user.photoURL
    }
    return userRef.set(data, { merge: true })
  }

  signOut() {
    this.afAuth.auth.signOut().then(() => {
      window.location.reload()
    });
  }
}
