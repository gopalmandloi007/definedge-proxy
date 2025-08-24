from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse
import json
import os

app = FastAPI()

# ---------------- OAuth Config ----------------
CLIENT_ID = "TRPW"
REDIRECT_URI = "https://definedge-proxy.onrender.com/callback"
AUTH_URL = "https://signin.definedgesecurities.com/auth/realms/debroking/protocol/openid-connect/auth"
TOKEN_URL = "https://signin.definedgesecurities.com/auth/realms/debroking/protocol/openid-connect/token"

# ---------------- All Definedge URLs ----------------
PAGE_URLS = {
    "Definedge Login": AUTH_URL,
    "Authenticate OTP": "https://signin.definedgesecurities.com/auth/realms/debroking/login-actions/authenticate",
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
    for name, url in PAGE_URLS.items():
        links += f'<li><a href="/open/{name}">{name}</a></li>'
    links += "</ul>"
    return f"<h2>Definedge Proxy</h2><p>Open any page via Render (office network safe)</p>{links}"

# ---------------- Open Page via Proxy ----------------
@app.get("/open/{page_name}")
async def open_page(page_name: str):
    if page_name not in PAGE_URLS:
        return {"error": "Page not found"}
    return RedirectResponse(PAGE_URLS[page_name])

# ---------------- Login Callback ----------------
@app.get("/callback")
async def callback(code: str = None, state: str = None):
    if not code:
        return {"error": "No code received"}
    # token logic placeholder
    # save token.json if needed
    return {"message": "Login callback received, code saved."}
