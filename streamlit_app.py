import streamlit as st
import webbrowser

# --- Pre-mapped pages same as app.py ---
PAGES = {
    "Login to Definedge": "/login",
    "Chart": "chart",
    "Order Book": "orderbook",
    "GTT Orders": "gtt",
    "SIP Orders": "sip",
    "Basket Orders": "basket",
    "Trade Book": "tradebook",
    "Position Book": "positionbook",
    "Holdings Zone": "holdings_zone",
    "Limits": "limits",
    "Messages": "messages",
    "Market Analysis": "marketana",
    "Dashboard": "dashboard",
    "My Details": "mydetails",
    "Holdings": "holdings",
    "DP Holdings": "dpholdings",
    "Holding Insight": "holdingInsight",
    "History Payin/Payout": "historyPay",
    "Pay In": "payin",
    "Pay Out": "payout",
    "Fund Reallocation": "fundRealloc",
    "Realized P&L": "realized",
    "Unrealized P&L": "unrealized",
    "Tax P&L": "taxpnl",
    "PnL Insight": "pnlInsight",
    "Segmentwise PnL": "segmentPnl",
    "PnL Calendar": "pnlCalendar",
    "Mutual Fund PnL": "mutualfundPnl",
    "Ledger": "ledger",
    "Collateral": "collateral",
    "Trade Register": "tradeRegister",
    "FNO Trade Register": "FNOtradeRegister",
    "Daily Bill": "dailyBill",
    "Open Position": "openPosition",
    "Margin Client": "marginClient",
    "Sarathi Score": "sarathiScore",
    "Request": "request",
    "Feedback": "feedback",
}

# --- Your Render Proxy Base URL ---
RENDER_BASE = "https://definedge-proxy.onrender.com/open/"

# Streamlit UI
st.title("Definedge Proxy Frontend")
st.markdown(
    "Select any page from Definedge and open it through Render proxy (office network safe)."
)

page = st.selectbox("Choose Page", list(PAGES.keys()))

if st.button("Open Page"):
    page_code = PAGES[page]
    final_url = f"{RENDER_BASE}{page_code}"
    st.write(f"Opening: {final_url}")
    # Open in default browser
    webbrowser.open_new_tab(final_url)
