"""Zentickr - Yahoo Finance MCP server.

Exposes Yahoo Finance data (via yahooquery) as MCP tools: financial
statements, prices, valuation, ownership, analyst research, calendar
events, historical prices, and symbol search.
"""

import json
from datetime import datetime, timedelta
from typing import Any

import pandas as pd
from mcp.server.fastmcp import FastMCP
from yahooquery import Ticker, search

mcp = FastMCP("zentickr")


def _parse_symbols(symbols: str) -> list[str]:
    """Split a comma-separated symbol string into a clean uppercase list."""
    parsed = [s.strip().upper() for s in symbols.split(",") if s.strip()]
    if not parsed:
        raise ValueError("no stock symbols provided")
    return parsed


def convert_to_json_serializable(data: Any) -> Any:
    """Convert pandas objects (and containers of them) to JSON-serializable structures."""
    if isinstance(data, pd.DataFrame):
        if data.index.name or not isinstance(data.index, pd.RangeIndex):
            data = data.reset_index()
        return data.to_dict(orient="records")
    if isinstance(data, pd.Series):
        return data.to_dict()
    if isinstance(data, dict):
        return {k: convert_to_json_serializable(v) for k, v in data.items()}
    if isinstance(data, (list, tuple)):
        return [convert_to_json_serializable(item) for item in data]
    try:
        if pd.isna(data):
            return None
    except (TypeError, ValueError):
        pass  # array-likes where isna() is ambiguous pass through; json default=str handles them
    return data


def format_response(data: Any, title: str) -> str:
    """Format response data as a titled, pretty-printed JSON string."""
    json_data = convert_to_json_serializable(data)
    if json_data is None or (isinstance(json_data, (list, dict)) and len(json_data) == 0):
        return f"{title}: No data available"
    return f"{title}:\n{json.dumps(json_data, indent=2, default=str)}"


def _get(symbols: str, attr: str, title: str, **kwargs: Any) -> str:
    """Fetch a yahooquery Ticker attribute (calling it if callable) and format the result."""
    try:
        value = getattr(Ticker(_parse_symbols(symbols)), attr)
        if callable(value):
            value = value(**kwargs)
        return format_response(value, title)
    except Exception as exc:  # yahooquery raises many exception types; never leak a traceback
        return f"{title}: Error - {exc}"


@mcp.tool()
async def get_financial_data(symbols: str) -> str:
    """Get key financial data (price targets, margins, cash, debt, growth) for stock symbols.

    Args:
        symbols: Comma-separated stock symbols (e.g. "AAPL,GOOGL,MSFT")
    """
    return _get(symbols, "financial_data", "Financial Data")


@mcp.tool()
async def get_balance_sheet(symbols: str, frequency: str = "annual") -> str:
    """Get balance sheet data for stock symbols.

    Args:
        symbols: Comma-separated stock symbols
        frequency: "annual" or "quarterly"
    """
    return _get(symbols, "balance_sheet", f"Balance Sheet ({frequency})", frequency=frequency)


@mcp.tool()
async def get_cash_flow(symbols: str, frequency: str = "annual") -> str:
    """Get cash flow statement for stock symbols.

    Args:
        symbols: Comma-separated stock symbols
        frequency: "annual" or "quarterly"
    """
    return _get(symbols, "cash_flow", f"Cash Flow ({frequency})", frequency=frequency)


@mcp.tool()
async def get_income_statement(symbols: str, frequency: str = "annual") -> str:
    """Get income statement for stock symbols.

    Args:
        symbols: Comma-separated stock symbols
        frequency: "annual" or "quarterly"
    """
    return _get(symbols, "income_statement", f"Income Statement ({frequency})", frequency=frequency)


@mcp.tool()
async def get_valuation_measures(symbols: str) -> str:
    """Get valuation measures (market cap, P/E, EV, price/book) for stock symbols.

    Args:
        symbols: Comma-separated stock symbols
    """
    return _get(symbols, "valuation_measures", "Valuation Measures")


@mcp.tool()
async def get_earnings(symbols: str) -> str:
    """Get earnings data for stock symbols.

    Args:
        symbols: Comma-separated stock symbols
    """
    return _get(symbols, "earnings", "Earnings")


@mcp.tool()
async def get_earnings_trend(symbols: str) -> str:
    """Get earnings trend estimates for stock symbols.

    Args:
        symbols: Comma-separated stock symbols
    """
    return _get(symbols, "earnings_trend", "Earnings Trend")


@mcp.tool()
async def get_major_holders(symbols: str) -> str:
    """Get major holders breakdown for stock symbols.

    Args:
        symbols: Comma-separated stock symbols
    """
    return _get(symbols, "major_holders", "Major Holders")


@mcp.tool()
async def get_institution_ownership(symbols: str) -> str:
    """Get institutional ownership for stock symbols.

    Args:
        symbols: Comma-separated stock symbols
    """
    return _get(symbols, "institution_ownership", "Institution Ownership")


@mcp.tool()
async def get_insider_holders(symbols: str) -> str:
    """Get insider holders for stock symbols.

    Args:
        symbols: Comma-separated stock symbols
    """
    return _get(symbols, "insider_holders", "Insider Holders")


@mcp.tool()
async def get_insider_transactions(symbols: str) -> str:
    """Get insider transactions for stock symbols.

    Args:
        symbols: Comma-separated stock symbols
    """
    return _get(symbols, "insider_transactions", "Insider Transactions")


@mcp.tool()
async def get_fund_ownership(symbols: str) -> str:
    """Get mutual fund / ETF ownership for stock symbols.

    Args:
        symbols: Comma-separated stock symbols
    """
    return _get(symbols, "fund_ownership", "Fund Ownership")


@mcp.tool()
async def get_recommendations(symbols: str) -> str:
    """Get analyst recommendations for stock symbols.

    Args:
        symbols: Comma-separated stock symbols
    """
    return _get(symbols, "recommendations", "Recommendations")


@mcp.tool()
async def get_recommendation_trend(symbols: str) -> str:
    """Get analyst recommendation trend (strong buy/buy/hold/sell counts) for stock symbols.

    Args:
        symbols: Comma-separated stock symbols
    """
    return _get(symbols, "recommendation_trend", "Recommendation Trend")


@mcp.tool()
async def get_price_data(symbols: str) -> str:
    """Get current price and trading data for stock symbols.

    Args:
        symbols: Comma-separated stock symbols
    """
    return _get(symbols, "price", "Price Data")


@mcp.tool()
async def get_summary_detail(symbols: str) -> str:
    """Get summary details (day range, volume, dividend, 52-week range) for stock symbols.

    Args:
        symbols: Comma-separated stock symbols
    """
    return _get(symbols, "summary_detail", "Summary Detail")


@mcp.tool()
async def get_company_profile(symbols: str) -> str:
    """Get company profile (sector, industry, description, address) for stock symbols.

    Args:
        symbols: Comma-separated stock symbols
    """
    try:
        tickers = Ticker(_parse_symbols(symbols))
        combined = {
            "asset_profile": convert_to_json_serializable(tickers.asset_profile),
            "summary_profile": convert_to_json_serializable(tickers.summary_profile),
        }
        return format_response(combined, "Company Profile")
    except Exception as exc:
        return f"Company Profile: Error - {exc}"


@mcp.tool()
async def get_company_officers(symbols: str) -> str:
    """Get company officers (executives, titles, compensation) for stock symbols.

    Args:
        symbols: Comma-separated stock symbols
    """
    return _get(symbols, "company_officers", "Company Officers")


@mcp.tool()
async def get_technical_insights(symbols: str) -> str:
    """Get technical analysis insights for stock symbols.

    Args:
        symbols: Comma-separated stock symbols
    """
    return _get(symbols, "technical_insights", "Technical Insights")


@mcp.tool()
async def get_calendar_events(symbols: str) -> str:
    """Get upcoming calendar events (earnings dates, dividends) for stock symbols.

    Args:
        symbols: Comma-separated stock symbols
    """
    return _get(symbols, "calendar_events", "Calendar Events")


@mcp.tool()
async def get_esg_scores(symbols: str) -> str:
    """Get ESG (environmental, social, governance) scores for stock symbols.

    Args:
        symbols: Comma-separated stock symbols
    """
    return _get(symbols, "esg_scores", "ESG Scores")


@mcp.tool()
async def get_historical_prices(
    symbols: str,
    period: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    interval: str = "1d",
) -> str:
    """Get historical OHLCV price data for stock symbols.

    Args:
        symbols: Comma-separated stock symbols
        period: Time period ("1d","5d","1mo","3mo","6mo","1y","2y","5y","10y","max").
                Use either period or start_date/end_date, not both.
        start_date: Start date YYYY-MM-DD (defaults to one year ago)
        end_date: End date YYYY-MM-DD (defaults to today)
        interval: Interval ("1m","2m","5m","15m","30m","60m","90m","1d","5d","1wk","1mo","3mo")
    """
    title = f"Historical Price Data ({interval})"
    try:
        params: dict[str, Any] = {"interval": interval, "adj_timezone": True, "adj_ohlc": False}
        if period and not (start_date or end_date):
            params["period"] = period
        else:
            params["end"] = end_date or datetime.today().strftime("%Y-%m-%d")
            params["start"] = start_date or (datetime.today() - timedelta(days=365)).strftime(
                "%Y-%m-%d"
            )
        data = Ticker(_parse_symbols(symbols)).history(**params)
        if isinstance(data, pd.DataFrame) and not data.empty:
            data = data.reset_index()
            if "date" in data.columns:
                data["date"] = data["date"].astype(str)
            records = data.to_dict(orient="records")
            return f"{title}:\n{json.dumps(records, indent=2, default=str)}"
        return f"{title}: No data available"
    except Exception as exc:
        return f"{title}: Error - {exc}"


@mcp.tool()
async def search_symbols(query: str) -> str:
    """Search for stock symbols by company name or partial symbol.

    Args:
        query: Company name or partial ticker (e.g. "apple")
    """
    try:
        results = search(query)
        quotes = (results or {}).get("quotes", [])
        formatted = [
            {
                "symbol": q.get("symbol", ""),
                "name": q.get("longname", q.get("shortname", "")),
                "type": q.get("quoteType", ""),
                "exchange": q.get("exchange", ""),
            }
            for q in quotes[:10]
        ]
        if not formatted:
            return f"No results found for '{query}'"
        return f"Search Results for '{query}':\n{json.dumps(formatted, indent=2)}"
    except Exception as exc:
        return f"Symbol Search: Error - {exc}"


def main() -> None:
    """Run the Zentickr MCP server over stdio."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
