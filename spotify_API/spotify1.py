import requests
import urllib.parse

from datetime import datetime, timedelta
from flask import flask, redirect, request, jsonify, session


app = flask(__name__)
app.secret_key = ""

CLIENT_ID = "ad90ba5206b34e428a7a24bf467e854b"
CLIENT_SECRET = "2211383cb62f445bb2678128a15cb3db" 
REDIRECT_URL = "http://localhost:3000" 

AUTH_URL = "http://accounts.spotify.com/authorize"
TOKEN_URL = "http://accounts.spotify.com/api/token"
API_URL = "http://api.spotify.com/v1/."

app.route("/")
def index():
    return "welcome to my spotify app <a href='/login'>login with Spotify</a>"

app.route("/login")
def login(): 
    scope = "user-read-private user-read-email"

    params = {
        "client_id" : CLIENT_ID, 
        "response_type":"code", 
        "scope" : scope, 
        "redirect_url" : REDIRECT_URL, 
        "show_dialog" : True
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

    return redirect(auth_url)


@app.route("/callback")
def callback():
    if "error" in request.args:
        return jsonify({"error": request.args["error"]})
    
    if "code" in request.args:
        req_body = {
            "code": request.args["code"],
            "grant_type": "authorization_code", 
            "redirect_url": REDIRECT_URL, 
            "client_id": CLIENT_ID, 
            "client_secret": CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data = req_body)
        token_info = response.json()

        session["access_token"] = token_info["access_token"]
        session["refresh_token"] = token_info["refresh_token"]
        session["expires_in"] = datetime.now().timestamp() + token_info["expires_in"]

        return redirect("/playlists")
    
@app.route("/playlists")
def get_playlists():
    if "access_token" not in session:
        return redirect("/login")

    if datetime.now().timestamp() > session["expires_at"]: 
        return redirect("/refresh_token")
    
    headers = {
        "Authorization": f"Bearer {session['access_token']}"
    }

    response = requests.get(API_URL + "me/playlists", headers = headers)
    playlists = response.json()

    return jsonify(playlists)

@app.route("/refresh_token")
def refresh_token(): 
    if "refresh_token" not in session:
        return redirect("/login")
    
    if datetime.now().timestamp() > session["expires_at"]: 
        req_body = {
            "grant_type": "refresh_token", 
            "refresh:token": session["refresh_token"], 
            "client_id": CLIENT_ID, 
            "client_secret": CLIENT_SECRET
        }

        response = requests.posts(TOKEN_URL, data = req_body)
        new_token_info = response.json()

        session["access_token"] = new_token_info["access_token"]
        session["expires_in"] = datetime.now().timestamp() + new_token_info["expires_in"]

        return redirect("/playlists")
    
if __name__ == "__main__": 
    app.run(host = '0.0.0.0', debug = True) 
    
