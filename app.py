import os
import json
import uuid
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import httpx

app = FastAPI()

# ---------------- OAuth Config ----------------
CLIENT_ID = "TRPW"
REDIRECT_URI = "https://definedge-proxy.onrender.com/callback"
AUTH_URL = "https://signin.definedgesecurities.com/auth/realms/debroking/protocol/openid-connect/auth"
TOKEN_URL = "https://signin.definedgesecurities.com/auth/realms/debroking/protocol/openid-connect/token"

# ---------------- All Definedge URLs ----------------
PAGE_URLS = {
    "Chart": "https://zone.definedgesecurities.com/index.html#chart",
    "Order Book": "https://zone.definedgesecurities.com/index.html#trade:ob",
    "GTT Orders": "https://zone.definedgesecurities.com/index.html#trade:gtt",
    "SIP Orders": "https://zone.definedgesecurities.com/index.html#trade:sip",
    "Basket Orders": "https://zone.definedgesecurities.com/index.html#trade:bskt",
    "Trade Book": "https://zone.definedgesecurities.com/index.html#trade:tb",
    "Position Book": "https://zone.definedgesecurities.com/index.html#trade:ps",
    "Holdings": "https://zone.definedgesecurities.com/index.html#trade:hld",
    "Limits": "https://zone.definedgesecurities.com/index.html#trade:lmt",
    "Messages": "https://zone.definedgesecurities.com/index.html#trade:msg",
    "Market Analysis": "https://zone.definedgesecurities.com/index.html#trade:mktana",
    "My Account": "https://myaccount.definedgesecurities.com/",
    "My Details": "https://myaccount.definedgesecurities.com/mydetails",
    "Holdings Zone": "https://myaccount.definedgesecurities.com/holdings",
    "DP Holdings": "https://myaccount.definedgesecurities.com/dpHoldings",
    "Holding Insight": "https://myaccount.definedgesecurities.com/holdingInsight",
    "History Payin/Payout": "https://myaccount.definedgesecurities.com/historyOfPayinPayout",
    "Pay In": "https://myaccount.definedgesecurities.com/payIn",
    "Pay Out": "https://myaccount.definedgesecurities.com/payout",
    "Fund Reallocation": "https://myaccount.definedgesecurities.com/fund-reallocation",
    "Realized P&L": "https://myaccount.definedgesecurities.com/realized-P&L",
    "Unrealized P&L": "https://myaccount.definedgesecurities.com/unrealized-P&L",
    "Tax P&L": "https://myaccount.definedgesecurities.com/tax-P&L",
    "PnL Insight": "https://myaccount.definedgesecurities.com/PnLInsight",
    "Segmentwise PnL": "https://myaccount.definedgesecurities.com/SegmentwisePnL",
    "PnL Calendar": "https://myaccount.definedgesecurities.com/pnlCalendar",
    "Mutual Fund PnL": "https://myaccount.definedgesecurities.com/mutualFundPnL",
    "Ledger": "https://myaccount.definedgesecurities.com/ledger",
    "Collateral": "https://myaccount.definedgesecurities.com/collateral",
    "Trade Register": "https://myaccount.definedgesecurities.com/trade-register",
    "FNO Trade Register": "https://myaccount.definedgesecurities.com/FNO-trade-register",
    "Daily Bill": "https://myaccount.definedgesecurities.com/daily-bill",
    "Open Position": "https://myaccount.definedgesecurities.com/open-position",
    "Margin Client": "https://myaccount.definedgesecurities.com/margin-client",
    "Sarathi Score": "https://myaccount.definedgesecurities.com/sarathi-score",
    "Request": "https://myaccount.definedgesecurities.com/request",
    "Feedback": "https://myaccount.definedgesecurities.com/feedback",
}

# ---------------- Home Page ----------------
@app.get("/", response_class=HTMLResponse)
async def home():
    links = "<ul>"
    links += '<li><a href="/login">Login to Definedge</a></li>'
    for name in PAGE_URLS.keys():
        links += f'<li><a href="/open/{name.replace(" ", "_")}">{name}</a></li>'
    links += "</ul>"
    return f"<h2>Definedge Proxy</h2><p>Open any page via Render (office network safe)</p>{links}"

# ---------------- Login Endpoint ----------------
@app.get("/login")
async def login():
    state = str(uuid.uuid4())
    auth_url = (
        f"{AUTH_URL}?response_type=code&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}&state={state}&scope=openid"
    )
    return RedirectResponse(auth_url)

# ---------------- Callback Endpoint ----------------
@app.get("/callback")
async def callback(code: str = None, state: str = None):
    if not code:
        return {"error": "No code received"}
    
    # Exchange code for token
    async with httpx.AsyncClient() as client:
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        token_res = await client.post(TOKEN_URL, data=data, headers=headers)
    
    if token_res.status_code != 200:
        return {"error": "Token request failed", "detail": token_res.text}
    
    tokens = token_res.json()
    
    # Save token
    with open("token.json", "w") as f:
        json.dump(tokens, f, indent=4)
    
    return {"message": "Login successful! Tokens saved.", "tokens": tokens}

# ---------------- Open Page via Proxy ----------------
@app.get("/open/{page_name}")
async def open_page(page_name: str):
    # convert slug back to original
    page_key = page_name.replace("_", " ")
    if page_key not in PAGE_URLS:
        return {"error": "Page not found"}
    return RedirectResponse(PAGE_URLS[page_key])

# ---------------- Tokens Info ----------------
@app.get("/me")
async def me():
    if not os.path.exists("token.json"):
        return {"error": "No token found, please login first."}
    with open("token.json") as f:
        tokens = json.load(f)
    return tokens
