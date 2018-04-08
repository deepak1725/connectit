import { Component, OnInit } from '@angular/core';


declare const FB: any;

@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.css']
})
export class AuthComponent implements OnInit {

  constructor() { }
  FB:any;

  ngOnInit() {
    FB.getLoginStatus((response) => {
      this.statusChangeCallback(response);
      console.log("YEah it worked");
      
    });
  }

  statusChangeCallback = (response) => {
    console.log(response);
    let authResponse = response;
    if (response.status === 'connected') {
      // Logged into your app and Facebook.
      console.log('Logged in.');
      FB.api('/me', { fields: 'email,name,first_name,last_name' }, function (response) {
        console.log(response);
      });
      console.log("AR",response.authResponse);
      
      FB.api(
        `/${response.authResponse.userID}/groups`,
        function (response) {
          console.log("UserGroups", response);
          
          if (response && !response.error) {
            /* handle the result */
          }
        }
      );

    } else if (response.status === 'not_authorized') {
      // The person is logged into Facebook, but not your app.
      // document.getElementById('status').innerHTML = 'Please log ' +
      //     'into this app.';
      console.log("not Authorised");

    }
  }


  myFacebookLogin =  () => {
    FB.login(function (response) {
      if (response.status === 'connected') {
        console.log("Person Logged in", response);

        // Logged into your app and Facebook.
      } else {
        console.log("not Logged in", response);

        // The person is not logged into this app or we are unable to tell. 
      }
    }, { scope: 'publish_actions, public_profile, email, user_managed_groups'  });
  }

}
