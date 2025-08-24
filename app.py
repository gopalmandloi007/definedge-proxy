import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse
import httpx

app = FastAPI()

# --- OAuth Config ---
CLIENT_ID = "TRPW"
REDIRECT_URI = "https://definedge-proxy.onrender.com/callback"
AUTH_URL = "https://signin.definedgesecurities.com/auth/realms/debroking/protocol/openid-connect/auth"
TOKEN_URL = "https://signin.definedgesecurities.com/auth/realms/debroking/protocol/openid-connect/token"

# --- ROOT ---
@app.get("/")
async def root():
    return {"message": "Definedge Proxy Running. Visit /login to start authentication."}

# --- LOGIN ---
@app.get("/login")
async def login():
    state = "xyz123"
    url = (
        f"{AUTH_URL}?response_type=code&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}&state={state}&scope=openid"
    )
    return RedirectResponse(url)

# --- CALLBACK ---
@app.get("/callback")
async def callback(request: Request, code: str = None, state: str = None):
    if not code:
        return {"error": "No code received"}

    async with httpx.AsyncClient() as client:
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        token_res = await client.post(TOKEN_URL, data=data, headers=headers)

    if token_res.status_code != 200:
        return {"error": "Token request failed", "detail": token_res.text}

    tokens = token_res.json()

    with open("token.json", "w") as f:
        json.dump(tokens, f, indent=4)

    return {"message": "Login successful! Tokens saved.", "tokens": tokens}

# --- ME ---
@app.get("/me")
async def me():
    if not os.path.exists("token.json"):
        return {"error": "No token found, please login first."}
    with open("token.json") as f:
        tokens = json.load(f)
    return tokens

# --- URL MAPPING ---
URLS = {
    # Zone Trading
    "chart": "https://zone.definedgesecurities.com/index.html#chart",
    "orderbook": "https://zone.definedgesecurities.com/index.html#trade:ob",
    "gtt": "https://zone.definedgesecurities.com/index.html#trade:gtt",
    "sip": "https://zone.definedgesecurities.com/index.html#trade:sip",
    "basket": "https://zone.definedgesecurities.com/index.html#trade:bskt",
    "tradebook": "https://zone.definedgesecurities.com/index.html#trade:tb",
    "positionbook": "https://zone.definedgesecurities.com/index.html#trade:ps",
    "holdings_zone": "https://zone.definedgesecurities.com/index.html#trade:hld",
    "limits": "https://zone.definedgesecurities.com/index.html#trade:lmt",
    "messages": "https://zone.definedgesecurities.com/index.html#trade:msg",
    "marketana": "https://zone.definedgesecurities.com/index.html#trade:mktana",

    # MyAccount BackOffice
    "dashboard": "https://myaccount.definedgesecurities.com/",
    "mydetails": "https://myaccount.definedgesecurities.com/mydetails",
    "holdings": "https://myaccount.definedgesecurities.com/holdings",
    "dpholdings": "https://myaccount.definedgesecurities.com/dpHoldings",
    "holdingInsight": "https://myaccount.definedgesecurities.com/holdingInsight",
    "historyPay": "https://myaccount.definedgesecurities.com/historyOfPayinPayout",
    "payin": "https://myaccount.definedgesecurities.com/payIn",
    "payout": "https://myaccount.definedgesecurities.com/payout",
    "fundRealloc": "https://myaccount.definedgesecurities.com/fund-reallocation",

    # PnL
    "realized": "https://myaccount.definedgesecurities.com/realized-P&L",
    "unrealized": "https://myaccount.definedgesecurities.com/unrealized-P&L",
    "taxpnl": "https://myaccount.definedgesecurities.com/tax-P&L",
    "pnlInsight": "https://myaccount.definedgesecurities.com/PnLInsight",
    "segmentPnl": "https://myaccount.definedgesecurities.com/SegmentwisePnL",
    "pnlCalendar": "https://myaccount.definedgesecurities.com/pnlCalendar",
    "mutualfundPnl": "https://myaccount.definedgesecurities.com/mutualFundPnL",

    # Ledger & Reports
    "ledger": "https://myaccount.definedgesecurities.com/ledger",
    "collateral": "https://myaccount.definedgesecurities.com/collateral",
    "tradeRegister": "https://myaccount.definedgesecurities.com/trade-register",
    "FNOtradeRegister": "https://myaccount.definedgesecurities.com/FNO-trade-register",
    "dailyBill": "https://myaccount.definedgesecurities.com/daily-bill",
    "openPosition": "https://myaccount.definedgesecurities.com/open-position",
    "marginClient": "https://myaccount.definedgesecurities.com/margin-client",

    # Others
    "sarathiScore": "https://myaccount.definedgesecurities.com/sarathi-score",
    "request": "https://myaccount.definedgesecurities.com/request",
    "feedback": "https://myaccount.definedgesecurities.com/feedback",
}

# --- DIRECT ROUTES ---
@app.get("/open/{page_name}")
async def open_page(page_name: str):
    url = URLS.get(page_name)
    if not url:
        return {"error": "Invalid page name"}
    return RedirectResponse(url)
