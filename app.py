from fastapi import FastAPI, Request
import httpx

app = FastAPI()

# ---- Allowed Definedge URLs ----
ALLOWED_URLS = {
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

    # MyAccount (Back Office)
    "dashboard": "https://myaccount.definedgesecurities.com/",
    "mydetails": "https://myaccount.definedgesecurities.com/mydetails",
    "holdings": "https://myaccount.definedgesecurities.com/holdings",
    "dpholdings": "https://myaccount.definedgesecurities.com/dpHoldings",
    "holdingInsight": "https://myaccount.definedgesecurities.com/holdingInsight",

    # Funds
    "payin": "https://myaccount.definedgesecurities.com/payIn",
    "payout": "https://myaccount.definedgesecurities.com/payout",
    "fundrealloc": "https://myaccount.definedgesecurities.com/fund-reallocation",
    "fundhistory": "https://myaccount.definedgesecurities.com/historyOfPayinPayout",

    # PnL
    "realized": "https://myaccount.definedgesecurities.com/realized-P&L",
    "unrealized": "https://myaccount.definedgesecurities.com/unrealized-P&L",
    "taxpnl": "https://myaccount.definedgesecurities.com/tax-P&L",
    "pnlinsight": "https://myaccount.definedgesecurities.com/PnLInsight",
    "segmentpnl": "https://myaccount.definedgesecurities.com/SegmentwisePnL",
    "pnlcalendar": "https://myaccount.definedgesecurities.com/pnlCalendar",
    "mutualfundpnl": "https://myaccount.definedgesecurities.com/mutualFundPnL",

    # Ledger & Reports
    "ledger": "https://myaccount.definedgesecurities.com/ledger",
    "collateral": "https://myaccount.definedgesecurities.com/collateral",
    "traderegister": "https://myaccount.definedgesecurities.com/trade-register",
    "fnotraderegister": "https://myaccount.definedgesecurities.com/FNO-trade-register",
    "dailybill": "https://myaccount.definedgesecurities.com/daily-bill",
    "openposition": "https://myaccount.definedgesecurities.com/open-position",
    "marginclient": "https://myaccount.definedgesecurities.com/margin-client",

    # Others
    "sarathi": "https://myaccount.definedgesecurities.com/sarathi-score",
    "request": "https://myaccount.definedgesecurities.com/request",
    "feedback": "https://myaccount.definedgesecurities.com/feedback",
}

# ---- Proxy Endpoint ----
@app.get("/open/{name}")
async def proxy_open(name: str, request: Request):
    if name not in ALLOWED_URLS:
        return {"error": "URL not allowed"}
    
    target_url = ALLOWED_URLS[name]
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(target_url)
    
    return resp.text
