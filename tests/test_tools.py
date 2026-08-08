import json

import pandas as pd
import pytest

import zentickr.server as server

EXPECTED_TOOLS = {
    "get_financial_data",
    "get_balance_sheet",
    "get_cash_flow",
    "get_income_statement",
    "get_valuation_measures",
    "get_earnings",
    "get_earnings_trend",
    "get_major_holders",
    "get_institution_ownership",
    "get_insider_holders",
    "get_insider_transactions",
    "get_fund_ownership",
    "get_recommendations",
    "get_recommendation_trend",
    "get_price_data",
    "get_summary_detail",
    "get_company_profile",
    "get_company_officers",
    "get_technical_insights",
    "get_calendar_events",
    "get_esg_scores",
    "get_historical_prices",
    "search_symbols",
}


async def test_all_tools_registered():
    tools = await server.mcp.list_tools()
    assert {t.name for t in tools} == EXPECTED_TOOLS


def test_parse_symbols_cleans_input():
    assert server._parse_symbols(" aapl, msft ,GOOGL") == ["AAPL", "MSFT", "GOOGL"]


def test_parse_symbols_rejects_empty():
    with pytest.raises(ValueError):
        server._parse_symbols(" , ")


class StubTicker:
    """Records constructor args and serves canned attributes."""

    last_symbols = None
    last_history_kwargs = None
    financial_data = {"AAPL": {"currentPrice": 1.0}}

    def __init__(self, symbols):
        StubTicker.last_symbols = symbols

    def history(self, **kwargs):
        import pandas as pd

        StubTicker.last_history_kwargs = kwargs
        return pd.DataFrame()


async def test_get_financial_data_formats_stub(monkeypatch):
    monkeypatch.setattr(server, "Ticker", StubTicker)
    out = await server.get_financial_data("aapl")
    assert out.startswith("Financial Data:")
    assert "currentPrice" in out
    assert StubTicker.last_symbols == ["AAPL"]


async def test_tool_returns_error_string_when_yahooquery_fails(monkeypatch):
    class ExplodingTicker:
        def __init__(self, symbols):
            raise RuntimeError("boom")

    monkeypatch.setattr(server, "Ticker", ExplodingTicker)
    out = await server.get_price_data("AAPL")
    assert out == "Price Data: Error - boom"


async def test_empty_symbols_return_error_not_traceback():
    out = await server.get_financial_data(" , ")
    assert out.startswith("Financial Data: Error -")


async def test_historical_prices_uses_period(monkeypatch):
    monkeypatch.setattr(server, "Ticker", StubTicker)
    await server.get_historical_prices("AAPL", period="6mo", interval="1d")
    assert StubTicker.last_history_kwargs["period"] == "6mo"
    assert "start" not in StubTicker.last_history_kwargs


async def test_historical_prices_uses_date_range(monkeypatch):
    monkeypatch.setattr(server, "Ticker", StubTicker)
    await server.get_historical_prices("AAPL", start_date="2025-01-01", end_date="2025-06-30")
    assert StubTicker.last_history_kwargs["start"] == "2025-01-01"
    assert StubTicker.last_history_kwargs["end"] == "2025-06-30"
    assert "period" not in StubTicker.last_history_kwargs


def strict_payload(response: str):
    """Parse the JSON body of a tool response, rejecting NaN/Infinity literals."""

    def reject(constant):
        raise ValueError(f"not valid JSON: {constant}")

    return json.loads(response.split(":\n", 1)[1], parse_constant=reject)


def test_dataframe_missing_cells_serialize_as_null():
    frame = pd.DataFrame({"eps": [1.5, float("nan")], "note": ["ok", None]})
    payload = strict_payload(server.format_response(frame, "T"))
    assert payload == [{"eps": 1.5, "note": "ok"}, {"eps": None, "note": None}]


def test_series_missing_values_serialize_as_null():
    series = pd.Series({"trailingPE": 30.1, "forwardPE": float("nan")})
    payload = strict_payload(server.format_response(series, "T"))
    assert payload == {"trailingPE": 30.1, "forwardPE": None}


async def test_historical_prices_missing_cells_serialize_as_null(monkeypatch):
    class NanHistoryTicker:
        def __init__(self, symbols):
            pass

        def history(self, **kwargs):
            index = pd.MultiIndex.from_tuples([("AAPL", "2025-01-02")], names=["symbol", "date"])
            return pd.DataFrame({"close": [1.0], "adjclose": [float("nan")]}, index=index)

    monkeypatch.setattr(server, "Ticker", NanHistoryTicker)
    out = await server.get_historical_prices("AAPL", period="5d")
    assert strict_payload(out) == [
        {"symbol": "AAPL", "date": "2025-01-02", "close": 1.0, "adjclose": None}
    ]
