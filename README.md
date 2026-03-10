# stock-data-skill

CLI tool and OpenClaw skill for stock/crypto data analysis. Provides 47 data tools covering A-shares, HK stocks, US stocks, and cryptocurrencies with multi-source failover.

## Install

```bash
# Via pip
pip install stock-data-skill
```

## Usage

```bash
# List all 47 available tools
stock-data --list

# A-share examples
stock-data stock_prices symbol=600519 market=sh limit=60
stock-data stock_realtime symbol=600519 market=sh
stock-data search keyword=茅台
stock-data stock_chip symbol=300058
stock-data stock_fund_flow symbol=300058

# US stock
stock-data stock_overview_us symbol=AAPL
stock-data stock_prices_global symbol=AAPL market=us limit=30

# Crypto
stock-data okx_prices instId=BTC-USDT bar=1D limit=60
stock-data binance_ai_report symbol=BTC

# Market overview
stock-data stock_news_global

# Health Check
stock-data data_source_status
```

## Configuration
For standalone CLI usage, set environment variables in your shell:

```bash
export TUSHARE_TOKEN=your_token
export ALPHA_VANTAGE_API_KEY=your_key
```

OpenClaw automatically loads environment variables from `~/.openclaw/.env`. Copy the example file and fill in your API keys:

```bash
cp .env.example ~/.openclaw/.env
# Edit ~/.openclaw/.env with your keys
```

See `.env.example` for all supported variables and how to obtain API keys.

## OpenClaw Skill

Manually copy to your skills directory:

```bash
cp -r SKILL.md references/ ~/.openclaw/workspace/skills/stock-data/
```

## Tool Categories

| Category | Count | Examples |
|----------|-------|---------|
| A-Stock Price & Quotes | 3 | stock_prices, stock_realtime, stock_batch_realtime |
| A-Stock Info & Search | 4 | search, stock_info, stock_indicators, get_current_time |
| A-Stock Market Flow | 7 | stock_zt_pool, stock_north_flow, stock_margin_trading |
| A-Stock Analysis | 5 | stock_chip, stock_fund_flow, stock_sector_spot |
| A-Stock Valuation | 7 | stock_valuation_compare, stock_dividend_history |
| A-Stock Shareholders | 4 | stock_locked_shares, stock_top10_holders |
| A-Stock Quant | 3 | stock_screener, trading_signals, backtest_strategy |
| US/HK Stock | 7 | stock_overview_us, stock_financials_us |
| Crypto | 4 | okx_prices, okx_loan_ratios, binance_ai_report |
| Market & System | 3 | stock_news, stock_news_global, data_source_status |

## License

MIT
