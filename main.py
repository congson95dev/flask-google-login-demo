# server.py
import json
import os
import requests

from authlib.integrations.flask_client import OAuth
from flask import Flask, abort, redirect, render_template, session, url_for

app = Flask(__name__)

appConf = {
    "OAUTH2_CLIENT_ID": os.environ.get("GOOGLE_CLIENT_ID"),
    "OAUTH2_CLIENT_SECRET": os.environ.get("GOOGLE_CLIENT_SECRET"),
    "OAUTH2_META_URL": "https://accounts.google.com/.well-known/openid-configuration",
    "FLASK_SECRET": "ALongRandomlyGeneratedString",
    "FLASK_PORT": 5000
}

app.secret_key = appConf.get("FLASK_SECRET")

oauth = OAuth(app)
oauth.register(
    "myApp",
    client_id=appConf.get("OAUTH2_CLIENT_ID"),
    client_secret=appConf.get("OAUTH2_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'{appConf.get("OAUTH2_META_URL")}',
    authorize_params={'access_type': 'offline'}, # add this to get refresh_token
)


@app.route("/")
def home():
    return render_template("home.html", session=session.get("user"),
                           pretty=json.dumps(session.get("user"), indent=4))


# callback url
@app.route("/signin-google")
def googleCallback():
    token = oauth.myApp.authorize_access_token()
    session["user"] = token
    return redirect(url_for("home"))


# login url
@app.route("/google-login")
def googleLogin():
    # redirect to google api and when success, it will redirect to our callback url
    # the flow will automatic handle by authorize_redirect()
    return oauth.myApp.authorize_redirect(redirect_uri=url_for("googleCallback", _external=True))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))


@app.route("/refresh")
def refreshToken():
    refresh_token = session["user"]["refresh_token"]
    params = {
        "grant_type": "refresh_token",
        "client_id": appConf.get("OAUTH2_CLIENT_ID"),
        "client_secret": appConf.get("OAUTH2_CLIENT_SECRET"),
        "refresh_token": refresh_token
    }

    authorization_url = "https://oauth2.googleapis.com/token"

    r = requests.post(authorization_url, data=params)

    if r.ok:
        return r.json()['access_token']
    else:
        return None


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=appConf.get(
        "FLASK_PORT"), debug=True)
