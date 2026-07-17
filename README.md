<div align="center"><img src="https://raw.githubusercontent.com/ChintanDiwakar/zentickr-yahoo-query-mcp/refs/heads/main/avatar.png" alt="Zentickr Logo" width="200" height="200" /></div>

# Zentickr — Yahoo Finance MCP Server

Zentickr is a stdio-based Model Context Protocol (MCP) server that gives AI assistants access to 23 Yahoo Finance tools through the `yahooquery` library—covering prices, fundamentals, statements, analyst research, ownership, events, and symbol discovery.

[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/chintan-diwakar/zentickr-yahoo-query-mcp/actions/workflows/quality.yml/badge.svg)](https://github.com/chintan-diwakar/zentickr-yahoo-query-mcp/actions/workflows/quality.yml)
[![Python >=3.10](https://img.shields.io/badge/Python-%3E%3D3.10-blue.svg)](https://www.python.org/)

## ⚠️ Important Disclaimer

This software is provided for educational and informational purposes only. It does not provide financial, investment, legal, or tax advice. Market data may be delayed, incomplete, or inaccurate. You are solely responsible for your investment decisions; the authors are not liable for any losses or damages arising from use of this software.

## Quickstart

```bash
git clone https://github.com/chintan-diwakar/zentickr-yahoo-query-mcp.git
cd zentickr-yahoo-query-mcp
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

Run the server over stdio:

```bash
zentickr
```

Or:

```bash
python -m zentickr
```

## Client setup

### Claude Desktop

Add this to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "zentickr": {
      "command": "/absolute/path/to/zentickr-yahoo-query-mcp/.venv/bin/zentickr"
    }
  }
}
```

### Claude Code

```bash
claude mcp add zentickr -- /absolute/path/to/zentickr-yahoo-query-mcp/.venv/bin/zentickr
```

### Cursor

Create or update `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "zentickr": {
      "command": "/absolute/path/to/zentickr-yahoo-query-mcp/.venv/bin/zentickr"
    }
  }
}
```

## Real-world use cases

### Compare Apple and Microsoft fundamentals

**Prompt:** “Compare Apple and Microsoft fundamentals.”

The assistant can call `get_financial_data(symbols="AAPL,MSFT")` and `get_valuation_measures(symbols="AAPL,MSFT")`.

Captured output excerpt:

```json
Financial Data:
{
  "AAPL": {
    "currentPrice": 333.26,
    "targetHighPrice": 400.0,
    "targetLowPrice": 215.0,
    "targetMeanPrice": 315.78604,
    "recommendationKey": "buy",
    "numberOfAnalystOpinions": 43,
    "totalCash": 68507000832,
    "totalDebt": 84710998016,
    "totalRevenue": 451442016256,
    "earningsGrowth": 0.218,
    "revenueGrowth": 0.166
  }
}
```

```json
Valuation Measures:
[
  {
    "symbol": "AAPL",
    "asOfDate": "2024-06-10 00:00:00",
    "periodType": "TTM",
    "ForwardPeRatio": 26.2467,
    "MarketCap": 2961317915840.0,
    "PbRatio": 39.913172,
    "PeRatio": 30.034215,
    "PegRatio": 2.0439
  }
]
```

### Prep me for AAPL earnings

**Prompt:** “Prep me for AAPL earnings.”

The assistant can call `get_calendar_events(symbols="AAPL")` and `get_earnings_trend(symbols="AAPL")`.

Captured output excerpts:

```json
Calendar Events:
{
  "AAPL": {
    "earnings": {
      "earningsDate": [
        "2026-07-31 01:30:S"
      ],
      "earningsAverage": 1.89396,
      "earningsLow": 1.83,
      "earningsHigh": 1.99,
      "revenueAverage": 108890141050
    }
  }
}
```

```json
Earnings Trend:
{
  "AAPL": {
    "trend": [
      {
        "period": "0q",
        "endDate": "2026-06-30",
        "growth": 0.20629999,
        "earningsEstimate": {
          "avg": 1.89396,
          "numberOfAnalysts": 31,
          "yearAgoEps": 1.57
        }
      }
    ]
  }
}
```

### Find NVIDIA's ticker and current price

**Prompt:** “Find NVIDIA's ticker and current price.”

The assistant can call `search_symbols(query="nvidia")`, then `get_price_data(symbols="NVDA")`.

Captured output excerpts:

```json
Search Results for 'nvidia':
[
  {
    "symbol": "NVDA",
    "name": "NVIDIA Corporation",
    "type": "EQUITY",
    "exchange": "NMS"
  }
]
```

```json
Price Data:
{
  "NVDA": {
    "preMarketPrice": 202.155,
    "regularMarketPrice": 207.4,
    "regularMarketDayHigh": 211.08,
    "regularMarketDayLow": 205.85,
    "regularMarketVolume": 116253420,
    "regularMarketPreviousClose": 212.5,
    "exchangeName": "NasdaqGS",
    "marketState": "PRE",
    "symbol": "NVDA"
  }
}
```

## Tool catalog

### Market Data

| Tool | Arguments | Returns |
|---|---|---|
| `get_price_data` | `symbols: str` | Current price and trading data |
| `get_summary_detail` | `symbols: str` | Day range, volume, dividend, and 52-week range |
| `get_historical_prices` | `symbols: str`, `period: str \| None = None`, `start_date: str \| None = None`, `end_date: str \| None = None`, `interval: str = "1d"` | Historical OHLCV price data |
| `get_calendar_events` | `symbols: str` | Upcoming earnings dates and dividend events |

### Financial Statements

| Tool | Arguments | Returns |
|---|---|---|
| `get_financial_data` | `symbols: str` | Key financial data, including targets, margins, cash, debt, and growth |
| `get_balance_sheet` | `symbols: str`, `frequency: str = "annual"` | Balance sheet data |
| `get_cash_flow` | `symbols: str`, `frequency: str = "annual"` | Cash flow statement |
| `get_income_statement` | `symbols: str`, `frequency: str = "annual"` | Income statement |
| `get_valuation_measures` | `symbols: str` | Market cap, P/E, EV, and price/book measures |
| `get_earnings` | `symbols: str` | Earnings data |
| `get_earnings_trend` | `symbols: str` | Earnings trend estimates |

### Analysis & Research

| Tool | Arguments | Returns |
|---|---|---|
| `get_recommendations` | `symbols: str` | Analyst recommendations |
| `get_recommendation_trend` | `symbols: str` | Strong buy, buy, hold, sell, and strong sell counts |
| `get_technical_insights` | `symbols: str` | Technical analysis insights |
| `get_esg_scores` | `symbols: str` | Environmental, social, and governance scores |
| `get_company_profile` | `symbols: str` | Company sector, industry, description, and address |

### Ownership & Governance

| Tool | Arguments | Returns |
|---|---|---|
| `get_major_holders` | `symbols: str` | Major holders breakdown |
| `get_institution_ownership` | `symbols: str` | Institutional ownership |
| `get_insider_holders` | `symbols: str` | Insider holders |
| `get_insider_transactions` | `symbols: str` | Insider transactions |
| `get_fund_ownership` | `symbols: str` | Mutual fund and ETF ownership |
| `get_company_officers` | `symbols: str` | Executives, titles, and compensation |

### Discovery

| Tool | Arguments | Returns |
|---|---|---|
| `search_symbols` | `query: str` | Matching stock symbols by company name or partial ticker |

`symbols` is a comma-separated string, such as `"AAPL,GOOGL,MSFT"`. Statement frequency accepts `"annual"` or `"quarterly"`.

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run the offline test suite and linter:

```bash
pytest
ruff check .
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full contribution guide.

## Data source

Data is sourced from Yahoo Finance through the unofficial [`yahooquery`](https://github.com/dpguthrie/yahooquery) library. It is subject to Yahoo's terms and no API key is required.

## License

MIT — see [LICENSE](LICENSE).

## Support

Please open a [GitHub Issue](https://github.com/chintan-diwakar/zentickr-yahoo-query-mcp/issues).
