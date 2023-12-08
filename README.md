# Flask Google Login Demo

This repo use as demo for google login by SSO (single sign on) using `authlib` library

## The flow of login:
we have `AppID`, `AppSecret`. we will use it to transfer as `client_id` and `client_secret`

click login

-> redirect to `google.com/authenticate?client_id=..&scope=..`<br>
-> render google login page, user input data and click on submit<br>
-> google check and provide us `authorize code` and redirect to callback url: `127.0.0.1:5000/auth-callback?authorize_code=..`<br>
-> from above url, we will redirect to `google.com/authorize?authorize_code=..&client_id=..&client_secret=..`<br>
-> google check and provide us `access token` and `refresh token`<br>

-> now, we use that access token to call to our `127.0.0.1:5000`

![flow.png](flow.png)

## Why call 2 time to google?

The first call is for authenticate, they will return authorize code, then in second call, they will return access token and refresh token.<br>
This is for improve the security.