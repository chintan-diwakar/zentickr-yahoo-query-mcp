#!/usr/bin/env python3
"""
Zentickr — Yahoo Finance MCP server.

An MCP server that provides access to Yahoo Finance data through yahooquery.
Exposes financial data, market information, and historical prices as tools.
"""

import json
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

from mcp.server.fastmcp import FastMCP
from yahooquery import Ticker
import pandas as pd

# Initialize the MCP server
mcp = FastMCP("zentickr")

# Helper function to convert pandas objects to JSON-serializable format
def convert_to_json_serializable(data: Any) -> Any:
    """Convert pandas DataFrames and other objects to JSON-serializable format."""
    if isinstance(data, pd.DataFrame):
        # Reset index to make it a column if it has meaningful data
        if data.index.name or not isinstance(data.index, pd.RangeIndex):
            data = data.reset_index()
        return data.to_dict(orient='records')
    elif isinstance(data, pd.Series):
        return data.to_dict()
    elif isinstance(data, dict):
        return {k: convert_to_json_serializable(v) for k, v in data.items()}
    elif isinstance(data, (list, tuple)):
        return [convert_to_json_serializable(item) for item in data]
    elif pd.isna(data):
        return None
    else:
        return data

# Helper function to format response
def format_response(data: Any, title: str) -> str:
    """Format the response data as a readable string."""
    try:
        json_data = convert_to_json_serializable(data)
        if json_data is None or (isinstance(json_data, list) and len(json_data) == 0):
            return f"{title}: No data available"
        
        # Pretty print JSON for readability
        return f"{title}:\n{json.dumps(json_data, indent=2, default=str)}"
    except Exception as e:
        return f"{title}: Error formatting data - {str(e)}"

@mcp.tool()
async def get_financial_data(symbols: str) -> str:
    """
    Get financial data for given stock symbols.
    
    Args:
        symbols: Comma-separated list of stock symbols (e.g., "AAPL,GOOGL,MSFT")
    """
    ticker_list = [s.strip().upper() for s in symbols.split(',')]
    tickers = Ticker(ticker_list)
    data = tickers.financial_data
    return format_response(data, "Financial Data")

@mcp.tool()
async def get_balance_sheet(symbols: str, frequency: str = "annual") -> str:
    """
    Get balance sheet data for given stock symbols.
    
    Args:
        symbols: Comma-separated list of stock symbols
        frequency: "annual" or "quarterly"
    """
    ticker_list = [s.strip().upper() for s in symbols.split(',')]
    tickers = Ticker(ticker_list)
    data = tickers.balance_sheet(frequency=frequency)
    return format_response(data, f"Balance Sheet ({frequency})")

@mcp.tool()
async def get_cash_flow(symbols: str, frequency: str = "annual") -> str:
    """
    Get cash flow statement for given stock symbols.
    
    Args:
        symbols: Comma-separated list of stock symbols
        frequency: "annual" or "quarterly"
    """
    ticker_list = [s.strip().upper() for s in symbols.split(',')]
    tickers = Ticker(ticker_list)
    data = tickers.cash_flow(frequency=frequency)
    return format_response(data, f"Cash Flow ({frequency})")

@mcp.tool()
async def get_income_statement(symbols: str, frequency: str = "annual") -> str:
    """
    Get income statement for given stock symbols.
    
    Args:
        symbols: Comma-separated list of stock symbols
        frequency: "annual" or "quarterly"
    """
    ticker_list = [s.strip().upper() for s in symbols.split(',')]
    tickers = Ticker(ticker_list)
    data = tickers.income_statement(frequency=frequency)
    return format_response(data, f"Income Statement ({frequency})")

@mcp.tool()
async def get_valuation_measures(symbols: str) -> str:
    """
    Get valuation measures for given stock symbols.
    
    Args:
        symbols: Comma-separated list of stock symbols
    """
    ticker_list = [s.strip().upper() for s in symbols.split(',')]
    tickers = Ticker(ticker_list)
    data = tickers.valuation_measures
    return format_response(data, "Valuation Measures")

@mcp.tool()
async def get_earnings(symbols: str) -> str:
    """
    Get earnings data for given stock symbols.
    
    Args:
        symbols: Comma-separated list of stock symbols
    """
    ticker_list = [s.strip().upper() for s in symbols.split(',')]
    tickers = Ticker(ticker_list)
    data = tickers.earnings
    return format_response(data, "Earnings")

@mcp.tool()
async def get_earnings_trend(symbols: str) -> str:
    """
    Get earnings trend data for given stock symbols.
    
    Args:
        symbols: Comma-separated list of stock symbols
    """
    ticker_list = [s.strip().upper() for s in symbols.split(',')]
    tickers = Ticker(ticker_list)
    data = tickers.earnings_trend
    return format_response(data, "Earnings Trend")

@mcp.tool()
async def get_major_holders(symbols: str) -> str:
    """
    Get major holders information for given stock symbols.
    
    Args:
        symbols: Comma-separated list of stock symbols
    """
    ticker_list = [s.strip().upper() for s in symbols.split(',')]
    tickers = Ticker(ticker_list)
    data = tickers.major_holders
    return format_response(data, "Major Holders")

@mcp.tool()
async def get_institution_ownership(symbols: str) -> str:
    """
    Get institutional ownership data for given stock symbols.
    
    Args:
        symbols: Comma-separated list of stock symbols
    """
    ticker_list = [s.strip().upper() for s in symbols.split(',')]
    tickers = Ticker(ticker_list)
    data = tickers.institution_ownership
    return format_response(data, "Institution Ownership")

@mcp.tool()
async def get_insider_holders(symbols: str) -> str:
    """
    Get insider holders information for given stock symbols.
    
    Args:
        symbols: Comma-separated list of stock symbols
    """
    ticker_list = [s.strip().upper() for s in symbols.split(',')]
    tickers = Ticker(ticker_list)
    data = tickers.insider_holders
    return format_response(data, "Insider Holders")

@mcp.tool()
async def get_insider_transactions(symbols: str) -> str:
    """
    Get insider transactions for given stock symbols.
    
    Args:
        symbols: Comma-separated list of stock symbols
    """
    ticker_list = [s.strip().upper() for s in symbols.split(',')]
    tickers = Ticker(ticker_list)
    data = tickers.insider_transactions
    return format_response(data, "Insider Transactions")

@mcp.tool()
async def get_fund_ownership(symbols: str) -> str:
    """
    Get fund ownership data for given stock symbols.
    
    Args:
        symbols: Comma-separated list of stock symbols
    """
    ticker_list = [s.strip().upper() for s in symbols.split(',')]
    tickers = Ticker(ticker_list)
    data = tickers.fund_ownership
    return format_response(data, "Fund Ownership")

@mcp.tool()
async def get_recommendations(symbols: str) -> str:
    """
    Get analyst recommendations for given stock symbols.
    
    Args:
        symbols: Comma-separated list of stock symbols
    """
    ticker_list = [s.strip().upper() for s in symbols.split(',')]
    tickers = Ticker(ticker_list)
    data = tickers.recommendations
    return format_response(data, "Recommendations")

@mcp.tool()
async def get_recommendation_trend(symbols: str) -> str:
    """
    Get recommendation trends for given stock symbols.
    
    Args:
        symbols: Comma-separated list of stock symbols
    """
    ticker_list = [s.strip().upper() for s in symbols.split(',')]
    tickers = Ticker(ticker_list)
    data = tickers.recommendation_trend
    return format_response(data, "Recommendation Trend")

@mcp.tool()
async def get_price_data(symbols: str) -> str:
    """
    Get current price data for given stock symbols.
    
    Args:
        symbols: Comma-separated list of stock symbols
    """
    ticker_list = [s.strip().upper() for s in symbols.split(',')]
    tickers = Ticker(ticker_list)
    data = tickers.price
    return format_response(data, "Price Data")

@mcp.tool()
async def get_summary_detail(symbols: str) -> str:
    """
    Get summary details for given stock symbols.
    
    Args:
        symbols: Comma-separated list of stock symbols
    """
    ticker_list = [s.strip().upper() for s in symbols.split(',')]
    tickers = Ticker(ticker_list)
    data = tickers.summary_detail
    return format_response(data, "Summary Detail")

@mcp.tool()
async def get_company_profile(symbols: str) -> str:
    """
    Get company profile information for given stock symbols.
    
    Args:
        symbols: Comma-separated list of stock symbols
    """
    ticker_list = [s.strip().upper() for s in symbols.split(',')]
    tickers = Ticker(ticker_list)
    
    # Combine asset_profile and summary_profile
    asset_profile = tickers.asset_profile
    summary_profile = tickers.summary_profile
    
    combined_data = {
        "asset_profile": convert_to_json_serializable(asset_profile),
        "summary_profile": convert_to_json_serializable(summary_profile)
    }
    
    return format_response(combined_data, "Company Profile")

@mcp.tool()
async def get_company_officers(symbols: str) -> str:
    """
    Get company officers information for given stock symbols.
    
    Args:
        symbols: Comma-separated list of stock symbols
    """
    ticker_list = [s.strip().upper() for s in symbols.split(',')]
    tickers = Ticker(ticker_list)
    data = tickers.company_officers
    return format_response(data, "Company Officers")

@mcp.tool()
async def get_technical_insights(symbols: str) -> str:
    """
    Get technical insights for given stock symbols.
    
    Args:
        symbols: Comma-separated list of stock symbols
    """
    ticker_list = [s.strip().upper() for s in symbols.split(',')]
    tickers = Ticker(ticker_list)
    data = tickers.technical_insights
    return format_response(data, "Technical Insights")

@mcp.tool()
async def get_calendar_events(symbols: str) -> str:
    """
    Get calendar events for given stock symbols.
    
    Args:
        symbols: Comma-separated list of stock symbols
    """
    ticker_list = [s.strip().upper() for s in symbols.split(',')]
    tickers = Ticker(ticker_list)
    data = tickers.calendar_events
    return format_response(data, "Calendar Events")

@mcp.tool()
async def get_esg_scores(symbols: str) -> str:
    """
    Get ESG (Environmental, Social, Governance) scores for given stock symbols.
    
    Args:
        symbols: Comma-separated list of stock symbols
    """
    ticker_list = [s.strip().upper() for s in symbols.split(',')]
    tickers = Ticker(ticker_list)
    data = tickers.esg_scores
    return format_response(data, "ESG Scores")

@mcp.tool()
async def get_historical_prices(
    symbols: str,
    period: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    interval: str = "1d"
) -> str:
    """
    Get historical price data for given stock symbols.
    
    Args:
        symbols: Comma-separated list of stock symbols
        period: Time period (e.g., "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "max").
                Either use period OR start_date/end_date, not both.
        start_date: Start date in YYYY-MM-DD format (optional if using period)
        end_date: End date in YYYY-MM-DD format (optional if using period)
        interval: Data interval ("1m", "2m", "5m", "15m", "30m", "60m", "90m", "1d", "5d", "1wk", "1mo", "3mo")
    """
    ticker_list = [s.strip().upper() for s in symbols.split(',')]
    tickers = Ticker(ticker_list)
    
    # Prepare parameters
    params = {
        "interval": interval,
        "adj_timezone": True,
        "adj_ohlc": False
    }
    
    # Use either period or date range
    if period and not (start_date or end_date):
        params["period"] = period
    else:
        # Use dates, defaulting to last year if not specified
        if not end_date:
            end_date = datetime.today().strftime('%Y-%m-%d')
        if not start_date:
            start_date = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
        
        params["start"] = start_date
        params["end"] = end_date
    
    data = tickers.history(**params)
    
    # Format the historical data with proper date handling
    if isinstance(data, pd.DataFrame) and not data.empty:
        # Reset index to include date and symbol as columns
        data = data.reset_index()
        
        # Convert date to string for JSON serialization
        if 'date' in data.columns:
            data['date'] = data['date'].astype(str)
        
        json_data = data.to_dict(orient='records')
        return f"Historical Price Data ({interval}):\n{json.dumps(json_data, indent=2, default=str)}"
    else:
        return "Historical Price Data: No data available"

@mcp.tool()
async def search_symbols(query: str) -> str:
    """
    Search for stock symbols by company name or partial symbol.
    
    Args:
        query: Search query (company name or partial symbol)
    """
    try:
        # Use Ticker's search functionality
        from yahooquery import search
        results = search(query)
        
        if results and 'quotes' in results:
            quotes = results['quotes']
            formatted_results = []
            
            for quote in quotes[:10]:  # Limit to top 10 results
                result = {
                    "symbol": quote.get('symbol', ''),
                    "name": quote.get('longname', quote.get('shortname', '')),
                    "type": quote.get('quoteType', ''),
                    "exchange": quote.get('exchange', '')
                }
                formatted_results.append(result)
            
            return f"Search Results for '{query}':\n{json.dumps(formatted_results, indent=2)}"
        else:
            return f"No results found for '{query}'"
    except Exception as e:
        return f"Error searching symbols: {str(e)}"

def main() -> None:
    """Run the Zentickr MCP server over stdio."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
