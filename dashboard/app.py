import streamlit as st

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from shared.config import get_settings
from data_providers.aws_api import AwsApiProvider
from services.market_data_service import MarketDataService

st.set_page_config(page_title="Stock Market Dashboard", layout="wide")

st.markdown(
    """
    <style>
      .small-muted { opacity: 0.75; font-size: 0.9rem; }
      .section-title { font-size: 1.1rem; font-weight: 650; margin-top: 0.25rem; }
      .card { padding: 1rem; border-radius: 14px; border: 1px solid rgba(255,255,255,0.08); }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Stock Market Dashboard On The Cloud")

DEFAULT_WATCHLIST = ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "TSLA", "META"]

settings = get_settings()
provider = AwsApiProvider(base_url=settings.aws_read_api_url)
service = MarketDataService(provider=provider)

st.sidebar.header("Settings")
symbol = st.sidebar.selectbox("Symbol", DEFAULT_WATCHLIST, index=0)
limit = st.sidebar.slider("History (days)", min_value=30, max_value=180, value=180, step=30)

st.sidebar.divider()

top_left, top_right = st.columns([1.2, 1])

try:
    quote = service.get_quote(symbol)
    history = service.get_history(symbol, limit=limit)

    with top_left:
        st.markdown('<div class="section-title">Overview</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)

        c1.metric("Symbol", quote.symbol)
        c2.metric("Price", f"${quote.price:,.2f}")
        c3.metric("Move", f"{quote.change_percent:+.2f}%", delta=f"{quote.change:+.2f}")

    with top_right:
        st.markdown('<div class="section-title">Watchlist Snapshot</div>', unsafe_allow_html=True)

        rows = []
        for s in DEFAULT_WATCHLIST:
            q = service.get_quote(s)
            rows.append(
                {
                    "Symbol": q.symbol,
                    "Price": round(q.price, 2),
                    "Change %": round(q.change_percent, 2),
                }
            )

        rows.sort(key=lambda r: abs(r["Change %"]), reverse=True)

        st.dataframe(
            rows,
            width='stretch',
            hide_index=True,
        )

    st.divider()

    st.markdown('<div class="section-title">Price History</div>', unsafe_allow_html=True)
    st.caption("Interact with chart to adjust scale")
    chart_data = [{"date": p.date, "close": p.close} for p in history.points]
    st.line_chart(chart_data, x="date", y="close", width='stretch')

    closes = [p.close for p in history.points]
    if len(closes) >= 2:
        start = closes[0]
        end = closes[-1]
        pct = ((end - start) / start) * 100 if start != 0 else 0.0

        a, b, c = st.columns(3)
        a.metric(f"{limit}d Return", f"{pct:+.2f}%")
        b.metric("Period High", f"${max(closes):,.2f}")
        c.metric("Period Low", f"${min(closes):,.2f}")

except Exception as e:
    st.error("Could not load data from your AWS Read API.")
    st.exception(e)
