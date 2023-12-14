# Flask Google Login Demo

This repo use as demo for google login by SSO (single sign on) using `authlib` library

Followed by this tutorial:<br>
https://www.youtube.com/watch?v=fZLWO3_V06Q

## The flow of login:
we have `AppID`, `AppSecret`. we will use it to transfer as `client_id` and `client_secret`

click login

-> redirect to `google.com/authenticate?client_id=..&scope=..`<br>
-> render google login page, user input data and click on submit<br>
-> google check and provide us `authorize code` and redirect to callback url: `127.0.0.1:5000/auth-callback?authorize_code=..`<br>
-> from above url, we will redirect to `google.com/authorize?authorize_code=..&client_id=..&client_secret=..`<br>
-> google check and provide us `access token` and `refresh token`<br>

-> now, we use that access token to call to our `127.0.0.1:5000`

## Detail of the explaination (this step was debugged in the authlib library):

click login<br>
`authlib` generate url:<br>
`https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=&redirect_uri=127.0.0.1:5000/auth-callback&scope=openid+profile+email&state=&nonce=&access_type=offline`
<br>redirect to that url, that url will show the login form of google

user input user name and password, click submit

google run api to generate `code` => this step is handle by google, we don't see how this step working

google redirect callback url:<br>
`127.0.0.1:5000/auth-callback?state=&code=&scope=email+profile+openid&authuser=0&prompt=consent`
<br>now we have `code`.

`authlib` generate url with below information:<br>
`https://oauth2.googleapis.com/token`
<br>method: `POST`
<br>headers = `{'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}`
<br>body = `"grant_type=authorization_code&redirect_uri=127.0.0.1:5000/auth-callback"`

redirect to that url

google check and generate access token and refresh token

![flow.png](flow.png)

## Why call 2 time to google?

The first call is for authenticate, they will return authorize code, then in second call, they will return access token and refresh token.<br>
This is for improve the security.