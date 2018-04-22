# ConnectIt [![Build Status](https://travis-ci.org/deepak1725/connectit.svg?branch=master)](https://travis-ci.org/deepak1725/connectit)

ConnectIt is a Web App Assignment, which aims to notify user about when certain event occurs.
These Events include:
a) When a new user follows him.
b) When his stream successfully goes up/down

## What it Does..??
1. Connect through Twitch
2. User is then showed the details we fetched from his Twitch Account.
3. On this Page user has a Option to Opt-In/Opt-Out of Email notifications about:

    a) When a new user follows him.
    b) When his stream successfully goes up/down
    
## What is Used to build ..??
1. I am Using Django 2.0 in Backend, and Angular 5 in Frontend.
2. For Signin Purposes, I am using Twitch OAuth2 Signin with scope of `user-read`.
3. For Emails, SendGrid is my Best Friend.

## Installation:

1. `git clone`
2. Activate Python Virtual Environment, and run `pip install -r requirements.txt` from Base project folder.
2. Make up a Twitch Dev Account with App Name any and Callback url as `http://localhost:8000/complete/twitch`at [Twitch Devs](https://dev.twitch.tv/)
3. Note up `client id` and `client secret` as provided in new Twitch App.
4. Paste this `client id` and `client secret` in settings.py, preferabbly make this as Environment variable
5. Similarly fill up SendGrid columns of `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` as SendGrid username and password respectively in settings.py

## Misc:
1. The Project is also hosted on Heroku and live Demo is available at [Live Demo](https://letsconnectit.herokuapp.com)

