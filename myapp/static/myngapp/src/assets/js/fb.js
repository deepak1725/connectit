$(function() {
    console.log("FB Initsa");
    FB.getLoginStatus(function (response) {
        statusChangeCallback(response);
    });
    

});


function statusChangeCallback(response) {
    console.log(response);
    
    if (response.status === 'connected') {
        // Logged into your app and Facebook.
        console.log('Logged in.');
    } else if (response.status === 'not_authorized') {
        // The person is logged into Facebook, but not your app.
        // document.getElementById('status').innerHTML = 'Please log ' +
        //     'into this app.';
        console.log("not Authorised");
        
    }
}  


function myFacebookLogin() {
    FB.login(function () { }, { scope: 'publish_actions' });
    // this.FB.login();
}