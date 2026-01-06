import streamlit as st
from shared.schemas import Quote, HistorySeries
from data_providers.aws_api import AwsApiProvider

#dashboard -> MarketDataService -> AVProvider -> AV api

class MarketDataService: #layer between dashborad and api, with caching

    def __init__(self, provider: AwsApiProvider):
        self.provider = provider

    def get_quote(self, symbol: str) -> Quote:
        return _get_quote_cached(self.provider.base_url, symbol.strip().upper())

    def get_history(self, symbol: str, limit: int = 180) -> HistorySeries:
        return _get_history_cached(self.provider.base_url, symbol.strip().upper(), int(limit))

@st.cache_data(ttl=60, show_spinner=False)
def _get_quote_cached(base_url: str, symbol: str) -> Quote:
    return AwsApiProvider(base_url=base_url).get_quote(symbol)

@st.cache_data(ttl=60 * 30, show_spinner=False)
def _get_history_cached(base_url: str, symbol: str, limit: int) -> HistorySeries:
    return AwsApiProvider(base_url=base_url).get_history(symbol, limit=limit)