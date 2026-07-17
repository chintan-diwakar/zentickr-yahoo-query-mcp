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
