# Stock Data CLI Tools Reference

All 47 tools. Invoke via:
```bash
stock-data <tool_name> key=value key2=value2
```

Common field defaults:
- `symbol` -- Stock code (digits or letters, e.g. 600519, AAPL, HK00700)
- `market` -- `sh`(Shanghai), `sz`(Shenzhen), `hk`(HK), `us`(US). Default: `sh`

---

## 1. A-Stock Price & Quotes

### stock_prices
Get historical prices with technical indicators. Supports A/HK/US, multi-source failover.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbol | str | *required* | Stock code |
| market | str | `sh` | sh/sz/hk/us |
| period | str | `daily` | daily or weekly (weekly not supported for US) |
| limit | int | `30` | Number of records to return |

```bash
stock-data stock_prices symbol=600519 market=sh period=daily limit=60
```

### stock_realtime
Get real-time quote for A-share or HK stock: latest price, change%, volume, turnover, PE, PB, etc.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbol | str | *required* | Stock code |
| market | str | `sh` | sh/sz/hk only |

```bash
stock-data stock_realtime symbol=600519 market=sh
```

### stock_batch_realtime
Batch real-time quotes for multiple A-shares.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbols | str | *required* | Comma-separated codes, e.g. 600519,000858,601318 |
| limit | int | `20` | Max number of stocks to return |

```bash
stock-data stock_batch_realtime symbols=600519,000858,601318 limit=10
```

---

## 2. A-Stock Info & Search

### search
Search stock by name/keyword. Covers A/HK/US/ETF. Slow -- skip if code is already known.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| keyword | str | *required* | Company name, stock name, or code |
| market | str | `sh` | sh/sz/hk/us |

```bash
stock-data search keyword=贵州茅台 market=sh
```

### stock_info
Get basic info for a stock (A/HK).

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbol | str | *required* | Stock code |
| market | str | `sh` | sh/sz/hk |

```bash
stock-data stock_info symbol=600519 market=sh
```

### stock_indicators
Get financial report key indicators. Supports A/HK/US.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbol | str | *required* | Stock code |
| market | str | `sh` | sh/sz/hk/us |

```bash
stock-data stock_indicators symbol=600519 market=sh
```

### get_current_time
Get current system time and nearby A-share trading days. No parameters.

```bash
stock-data get_current_time
```

---

## 3. A-Stock Market Flow

### stock_zt_pool
Get limit-up/strong/limit-down stock pools.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| pool_type | str | `涨停` | Pool type: 涨停 / 强势 / 跌停 / 昨日涨停 |
| date | str | `""` | Trade date YYYYMMDD, default latest trade day |
| limit | int | `50` | Number of records (30-100) |

```bash
stock-data stock_zt_pool pool_type=涨停 limit=30
```

### stock_lhb_ggtj_sina
Dragon-Tiger list (top active stocks) statistics. Multi-source.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| days | str | `5` | Recent days: 5/10/30/60 |
| limit | int | `50` | Number of records (30-100) |

```bash
stock-data stock_lhb_ggtj_sina days=5 limit=30
```

### stock_sector_fund_flow_rank
Sector fund flow ranking (industry/concept/region).

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| days | str | `今日` | Period: 今日 / 5日 / 10日 |
| cate | str | `行业资金流` | Category: 行业资金流 / 概念资金流 / 地域资金流 |

```bash
stock-data stock_sector_fund_flow_rank days=今日 cate=行业资金流
```

### stock_north_flow
Northbound capital flow (HKEX Connect). Key A-share market indicator.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| indicator | str | `北向资金` | Type: 北向资金 / 沪股通 / 深股通 |

```bash
stock-data stock_north_flow indicator=北向资金
```

### stock_margin_trading
Margin trading data. Individual stock or market-wide.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbol | str | `""` | Stock code (optional, empty = market-wide) |
| market | str | `sh` | sh / sz |
| limit | int | `30` | Number of records |

```bash
stock-data stock_margin_trading symbol=600519 market=sh limit=30
```

### stock_block_trade
Block trade data. Individual stock or market-wide.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbol | str | `""` | Stock code (optional, empty = market-wide) |
| limit | int | `50` | Number of records |

```bash
stock-data stock_block_trade symbol=600519 limit=20
```

### stock_holder_num
Shareholder count changes. Key indicator for chip concentration.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbol | str | *required* | Stock code, e.g. 300058, 600036 |

```bash
stock-data stock_holder_num symbol=300058
```

---

## 4. A-Stock Analysis

### stock_chip
Get chip distribution: profit ratio, avg cost, concentration, etc. A-shares only (not ETF/LOF).

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbol | str | *required* | A-share stock code |

```bash
stock-data stock_chip symbol=600519
```

### stock_period_stats
Multi-period statistics: cumulative change%, amplitude, turnover for 5/10/20/60/120 day windows.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbol | str | *required* | Stock code |
| market | str | `sh` | sh / sz |

```bash
stock-data stock_period_stats symbol=600519 market=sh
```

### stock_fund_flow
Individual stock fund flow: main force, super-large/large/medium/small order in/out.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbol | str | *required* | Stock code |

```bash
stock-data stock_fund_flow symbol=600519
```

### stock_sector_spot
Get sectors/boards a stock belongs to (industry + concept).

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbol | str | *required* | Stock code |

```bash
stock-data stock_sector_spot symbol=600519
```

### stock_board_cons
Get constituent stocks of an industry or concept board. Multi-source failover.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| board_name | str | *required* | Board name, e.g. 酿酒行业, 人工智能 |
| board_type | str | `industry` | industry or concept |
| limit | int | `30` | Number of records |

```bash
stock-data stock_board_cons board_name=酿酒行业 board_type=industry limit=20
```

---

## 5. A-Stock Valuation & Finance

### stock_valuation_compare
Individual stock valuation vs industry peers: PE/PB percentile ranking.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbol | str | *required* | Stock code |

```bash
stock-data stock_valuation_compare symbol=600519
```

### stock_market_pe_percentile
A-share market-wide PE/PB historical percentile. No parameters.

```bash
stock-data stock_market_pe_percentile
```

### stock_industry_pe
Industry PE comparison for sector rotation analysis.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| date | str | `""` | Date YYYYMMDD, default latest trade day |

```bash
stock-data stock_industry_pe date=20250210
```

### stock_dividend_history
Historical dividend/bonus records and yield analysis.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbol | str | *required* | Stock code |
| limit | int | `10` | Number of records |

```bash
stock-data stock_dividend_history symbol=600519 limit=10
```

### stock_institutional_holdings
Top mutual fund heavy holdings and position changes by quarter.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| date | str | `""` | Report period YYYYMMDD (e.g. 20240930), default latest quarter |
| limit | int | `30` | Number of records |

```bash
stock-data stock_institutional_holdings date=20240930 limit=30
```

### stock_earnings_calendar
Financial report disclosure schedule.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| period | str | `""` | Report period, e.g. 2024年报, 2024三季报. Default latest |
| limit | int | `50` | Number of records |

```bash
stock-data stock_earnings_calendar period=2024年报 limit=30
```

### stock_financial_compare
Detailed financial indicators: profitability, growth, solvency, operations, per-share metrics.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbol | str | *required* | Stock code |

```bash
stock-data stock_financial_compare symbol=600519
```

---

## 6. A-Stock Shareholders & Risk

### stock_locked_shares
Restricted share unlock calendar. Key supply pressure indicator.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| start_date | str | `""` | Start date YYYYMMDD, default today |
| end_date | str | `""` | End date YYYYMMDD, default today+30 |
| mode | str | `detail` | detail (per-stock) or summary (daily aggregate) |
| limit | int | `50` | Number of records |

```bash
stock-data stock_locked_shares start_date=20250211 end_date=20250311 mode=detail limit=30
```

### stock_pledge_ratio
Equity pledge data: industry breakdown or market trend.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| mode | str | `industry` | industry (by sector) or market (overall trend) |
| limit | int | `30` | Number of records |

```bash
stock-data stock_pledge_ratio mode=industry limit=20
```

### stock_top10_holders
Top 10 shareholders or top 10 free-float shareholders. Tracks ownership changes.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbol | str | *required* | Stock code |
| holder_type | str | `main` | main (top 10) or circulate (top 10 free-float) |
| limit | int | `30` | Number of records (multi-period) |

```bash
stock-data stock_top10_holders symbol=600519 holder_type=circulate
```

### portfolio_risk_analysis
Portfolio risk metrics: volatility, max drawdown, correlation matrix, Sharpe ratio.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbols | str | *required* | Comma-separated codes (min 2), e.g. 600519,000858,601318 |
| days | int | `60` | Analysis period in days |

```bash
stock-data portfolio_risk_analysis symbols=600519,000858,601318 days=60
```

---

## 7. A-Stock Quant

### stock_screener
Screen A-shares by PE, PB, market cap, change%, turnover, volume ratio.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| pe_min | float | `0` | Min dynamic PE |
| pe_max | float | `100` | Max dynamic PE (0 = no limit) |
| pb_min | float | `0` | Min PB |
| pb_max | float | `50` | Max PB (0 = no limit) |
| mc_min | float | `0` | Min market cap (hundred million CNY) |
| mc_max | float | `0` | Max market cap (0 = no limit) |
| change_min | float | `-100` | Min change% |
| change_max | float | `100` | Max change% |
| turnover_min | float | `0` | Min turnover% |
| volume_ratio_min | float | `0` | Min volume ratio |
| sort_by | str | `涨跌幅` | Sort field: 涨跌幅/换手率/量比/市盈率/市净率/总市值 |
| ascending | bool | `False` | Sort ascending |
| limit | int | `30` | Number of results |

```bash
stock-data stock_screener pe_min=5 pe_max=30 mc_min=100 sort_by=涨跌幅 limit=20
```

### trading_signals
Generate buy/sell signals from MACD, KDJ, RSI, Bollinger, moving averages, volume.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbol | str | *required* | Stock code |
| days | int | `60` | Analysis period in days |

```bash
stock-data trading_signals symbol=600519 days=60
```

### backtest_strategy
Backtest a trading strategy: returns, max drawdown, win rate, Sharpe, trade log.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbol | str | *required* | Stock code |
| strategy | str | `ma_cross` | ma_cross / macd / kdj / rsi / boll |
| start_date | str | `""` | Start YYYYMMDD, default 1 year ago |
| end_date | str | `""` | End YYYYMMDD, default today |
| initial_capital | float | `100000` | Initial capital (CNY) |
| ma_short | int | `5` | Short MA period (ma_cross only) |
| ma_long | int | `20` | Long MA period (ma_cross only) |

```bash
stock-data backtest_strategy symbol=600519 strategy=macd start_date=20240101 end_date=20241231
```

---

## 8. US/HK Stock

### stock_prices_global
Get US/HK historical prices with technical indicators. Multi-source failover.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbol | str | *required* | Stock code (e.g. AAPL, 00700) |
| market | str | `us` | us or hk |
| period | str | `daily` | daily or weekly |
| limit | int | `30` | Number of records |

```bash
stock-data stock_prices_global symbol=AAPL market=us period=daily limit=60
```

### stock_overview_us
US company fundamentals: market cap, PE, EPS, dividend yield, 52-week range, analyst ratings. Multi-source.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbol | str | *required* | US ticker, e.g. AAPL, MSFT, GOOGL, TSLA |

```bash
stock-data stock_overview_us symbol=AAPL
```

### stock_financials_us
US financial statements: balance sheet, income statement, cash flow. Multi-source.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbol | str | *required* | US ticker |
| report_type | str | `balance_sheet` | balance_sheet / income_statement / cash_flow |
| quarterly | bool | `True` | True for quarterly, False for annual |

```bash
stock-data stock_financials_us symbol=AAPL report_type=income_statement quarterly=True
```

### stock_news_us
US stock news with sentiment analysis. Requires ALPHA_VANTAGE_API_KEY.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbol | str | `""` | US ticker (optional, empty = market-wide news) |
| topics | str | `""` | Topic filter: technology, earnings, ipo, mergers_and_acquisitions, etc. |
| limit | int | `20` | Number of results (max 50) |

```bash
stock-data stock_news_us symbol=AAPL topics=earnings limit=10
```

### stock_earnings_us
US earnings history and analyst estimates. Multi-source.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbol | str | *required* | US ticker |

```bash
stock-data stock_earnings_us symbol=AAPL
```

### stock_insider_us
US insider trading records. Multi-source.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbol | str | *required* | US ticker |
| limit | int | `20` | Number of records |

```bash
stock-data stock_insider_us symbol=AAPL limit=10
```

### stock_tech_indicators_us
US stock technical indicators via Alpha Vantage. Requires ALPHA_VANTAGE_API_KEY.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbol | str | *required* | US ticker |
| indicator | str | `RSI` | SMA / EMA / RSI / MACD / BBANDS / STOCH / ADX / ATR |
| interval | str | `daily` | daily / weekly / monthly |
| time_period | int | `14` | Calculation period (e.g. RSI=14, SMA=20) |
| limit | int | `30` | Number of records |

```bash
stock-data stock_tech_indicators_us symbol=AAPL indicator=MACD interval=daily limit=30
```

---

## 9. Crypto

### okx_prices
OKX cryptocurrency K-line data with technical indicators. Auto-retry.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| instId | str | `BTC-USDT` | Product ID, e.g. BTC-USDT, ETH-USDT |
| bar | str | `1H` | Candle size: 1m/3m/5m/15m/30m/1H/2H/4H/6H/12H/1D/2D/3D/1W/1M/3M |
| limit | int | `100` | Number of candles (max 300, min recommended 30) |

```bash
stock-data okx_prices instId=BTC-USDT bar=1D limit=60
```

### okx_loan_ratios
OKX margin long/short ratio (borrowed quote vs base currency).

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbol | str | `BTC` | Currency: BTC, ETH, etc. |
| period | str | `1h` | Granularity: 5m / 1H / 1D |

```bash
stock-data okx_loan_ratios symbol=BTC period=1D
```

### okx_taker_volume
OKX taker buy/sell volume.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbol | str | `BTC` | Currency: BTC, ETH, etc. |
| period | str | `1h` | Granularity: 5m / 1H / 1D |
| instType | str | `SPOT` | Product type: SPOT (spot) / CONTRACTS (derivatives) |

```bash
stock-data okx_taker_volume symbol=ETH period=1H instType=CONTRACTS
```

### binance_ai_report
Binance AI analysis report for a cryptocurrency. Auto-retry.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbol | str | `BTC` | Crypto symbol: BTC, ETH, etc. |

```bash
stock-data binance_ai_report symbol=BTC
```

---

## 10. Market & System

### stock_news
Get recent news for a stock or crypto symbol.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| symbol | str | *required* | Stock code or crypto symbol |
| limit | int | `15` | Number of news items |

```bash
stock-data stock_news symbol=600519 limit=10
```

### stock_news_global
Get latest global financial news flash (Sina Finance + NewsNow). No parameters.

```bash
stock-data stock_news_global
```

### data_source_status
View multi-source provider status and circuit breaker info. No parameters.

```bash
stock-data data_source_status
```
