import os
from flask import Flask, redirect, request, session, url_for
import requests

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "supersecret")  # Render me set kar lena

# ---- CONFIG ----
CLIENT_ID = "TRPW"
REDIRECT_URI = "https://your-proxy.onrender.com/callback"  # apne render domain ka URL daalo
AUTH_BASE = "https://signin.definedgesecurities.com/auth/realms/debroking/protocol/openid-connect"
TOKEN_URL = f"{AUTH_BASE}/token"
AUTH_URL = f"{AUTH_BASE}/auth"

@app.route("/")
def home():
    return "Definedge Proxy Running. Visit /login to start authentication."

@app.route("/login")
def login():
    """ Step 1: Redirect user to Definedge login """
    state = os.urandom(8).hex()
    session["state"] = state
    url = (
        f"{AUTH_URL}?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&state={state}"
        f"&scope=openid"
    )
    return redirect(url)

@app.route("/callback")
def callback():
    """ Step 2: Handle redirect from Definedge with auth code """
    code = request.args.get("code")
    state = request.args.get("state")

    if not code or state != session.get("state"):
        return "Error: Invalid login response", 400

    # Step 3: Exchange code for token
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
    }

    resp = requests.post(TOKEN_URL, data=data)
    if resp.status_code != 200:
        return f"Token exchange failed: {resp.text}", 400

    token_data = resp.json()
    session["token"] = token_data
    return f"Login successful! Access Token: {token_data.get('access_token')[:30]}..."

@app.route("/me")
def me():
    """ Check session token """
    token = session.get("token")
    if not token:
        return redirect(url_for("login"))
    return token

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
