$(function() {
    
    FB.Event.subscribe('auth.login', function () {
        console.log('FB Event Auth login');
    });
});


