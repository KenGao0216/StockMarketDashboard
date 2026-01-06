import requests
from typing import Any, Dict, List

from shared.schemas import Quote, HistorySeries, HistoryPoint

class AwsApiProvider: #fetches from lambda funtcion read api
    def __init__(self, base_url: str, timeout_seconds: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout_seconds

    def get_quote(self, symbol: str) -> Quote:
        r = requests.get(
            f"{self.base_url}/quote",
            params={"symbol": symbol.strip().upper()},
            timeout=self.timeout,
        )
        r.raise_for_status()
        data: Dict[str, Any] = r.json()["data"]

        return Quote(
            symbol=data["symbol"],
            price=float(data["price"]),
            change=float(data["change"]),
            change_percent=float(data["changePercent"]),
            as_of=data.get("asOf", ""),
        )

    def get_history(self, symbol: str, limit: int = 180) -> HistorySeries:
        r = requests.get(
            f"{self.base_url}/history",
            params={"symbol": symbol.strip().upper(), "limit": str(limit)},
            timeout=self.timeout,
        )
        r.raise_for_status()
        payload: Dict[str, Any] = r.json()
        points_raw: List[Dict[str, Any]] = payload["points"]

        points = [
            HistoryPoint(symbol=p["symbol"], date=p["date"], close=float(p["close"]))
            for p in points_raw
        ]
        return HistorySeries(symbol=payload["symbol"], points=points)
