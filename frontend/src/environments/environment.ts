// This file can be replaced during build by using the `fileReplacements` array.
// `ng build --prod` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.

export const environment = {
  production: false,
  firebase: {
    apiKey: "AIzaSyCiZCbJyZm8VO4NKmiqHPA1EBntCLgktiQ",
    authDomain: "video-poker-202000.firebaseapp.com",
    databaseURL: "https://video-poker-202000.firebaseio.com",
    projectId: "video-poker-202000",
    storageBucket: "video-poker-202000.appspot.com",
    messagingSenderId: "193706581223",
    appId: "1:193706581223:web:789112463eb8ed5e2e5642",
    measurementId: "G-MKBPLEG3JB"
  },
  serverUrl: 'http://localhost:5000/api'
};

/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/dist/zone-error';  // Included with Angular CLI.
