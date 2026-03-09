# 数据源健康检查

对 stock-data-mcp 的所有数据源和工具进行全面健康检查。

### 检查步骤

#### 1. 数据源状态
调用 `data_source_status` 查看所有 Fetcher 和熔断器状态。

#### 2. A股验证（蓝色光标 300058）
逐一调用以下工具，记录成功/失败：
- `search` keyword=蓝色光标 market=sz
- `stock_info` symbol=300058 market=sz
- `stock_prices` symbol=300058 market=sz limit=5 （验证新增指标：ADX/CCI/WR/VWAP）
- `stock_realtime` symbol=300058 market=sz
- `stock_indicators` symbol=300058 market=sz
- `stock_chip` symbol=300058
- `stock_fund_flow` symbol=300058
- `stock_sector_spot` symbol=300058
- `stock_period_stats` symbol=300058
- `stock_batch_realtime` symbols=300058,000001
- `stock_zt_pool` pool_type=涨停 limit=5
- `stock_zt_pool` pool_type=强势 limit=5
- `stock_lhb_ggtj_sina` days=5 limit=5
- `stock_sector_fund_flow_rank` days=今日 cate=行业资金流
- `stock_board_cons` board_name=人工智能 board_type=concept limit=5
- `stock_north_flow` indicator=北向资金
- `stock_margin_trading` market=sh limit=5
- `stock_block_trade` limit=5
- `stock_holder_num` symbol=300058
- `stock_locked_shares` mode=detail limit=5
- `stock_pledge_ratio` mode=industry limit=5
- `stock_top10_holders` symbol=600519 holder_type=main
- `stock_valuation_compare` symbol=300058 （估值对比）
- `stock_dividend_history` symbol=600519 limit=5 （分红历史）
- `stock_financial_compare` symbol=300058 （财务指标详情）
- `stock_market_pe_percentile` （市场PE分位）
- `stock_industry_pe` （行业PE对比）
- `stock_institutional_holdings` limit=5 （基金重仓股）
- `stock_earnings_calendar` limit=5 （财报日历）
- `trading_signals` symbol=300058 days=60 （交易信号）
- `stock_screener` pe_max=30 limit=5 （选股器）
- `backtest_strategy` symbol=300058 strategy=ma_cross （策略回测）
- `portfolio_risk_analysis` symbols=300058,600519 days=30 （组合风险）

#### 3. 港股验证（阿里巴巴 09988）
- `stock_info` symbol=09988 market=hk
- `stock_prices` symbol=09988 market=hk limit=5
- `stock_indicators` symbol=09988 market=hk

#### 4. 美股验证（拼多多 PDD）
- `stock_prices` symbol=PDD market=us limit=5
- `stock_indicators` symbol=PDD market=us
- `stock_overview_us` symbol=PDD
- `stock_financials_us` symbol=PDD report_type=balance_sheet
- `stock_earnings_us` symbol=PDD
- `stock_insider_us` symbol=PDD limit=5

#### 5. 加密货币验证（BTC）
- `okx_prices` instId=BTC-USDT bar=1D limit=5
- `okx_loan_ratios` symbol=BTC period=1H
- `okx_taker_volume` symbol=BTC period=1H instType=SPOT
- `binance_ai_report` symbol=BTC

#### 6. 通用工具
- `get_current_time`
- `stock_news` symbol=300058 limit=3
- `stock_news_global`

### 输出格式

使用 Markdown 格式输出，便于阅读：

```markdown
## Stock Data MCP 健康检查报告
> 检查时间: {当前时间}

### 数据源状态

| Fetcher | 优先级 | 状态 |
|---------|-------|------|
| {fetcher1} | {priority1} | {status1} |
| {fetcher2} | {priority2} | {status2} |

### 熔断器状态

| 类型 | 状态 | 失败次数 |
|------|------|---------|
| {breaker1} | {state1} | {failures1} |
| {breaker2} | {state2} | {failures2} |

### A股工具测试

| 工具 | 状态 | 耗时(s) | 备注 |
|------|------|--------|------|
| search | {ok/fail} | {time1} | {note1} |
| stock_info | {ok/fail} | {time2} | {note2} |
| stock_prices | {ok/fail} | {time3} | 检查ADX/CCI/WR/VWAP列 |
| stock_realtime | {ok/fail} | {time4} | {note4} |
| stock_indicators | {ok/fail} | {time5} | {note5} |
| stock_chip | {ok/fail} | {time6} | {note6} |
| stock_fund_flow | {ok/fail} | {time7} | {note7} |
| stock_sector_spot | {ok/fail} | {time8} | {note8} |
| stock_period_stats | {ok/fail} | {time9} | {note9} |
| stock_batch_realtime | {ok/fail} | {time10} | {note10} |
| stock_zt_pool | {ok/fail} | {time11} | {note11} |
| stock_lhb_ggtj_sina | {ok/fail} | {time12} | {note12} |
| stock_sector_fund_flow_rank | {ok/fail} | {time13} | {note13} |
| stock_board_cons | {ok/fail} | {time14} | {note14} |
| stock_north_flow | {ok/fail} | {time15} | — |
| stock_margin_trading | {ok/fail} | {time16} | — |
| stock_block_trade | {ok/fail} | {time17} | — |
| stock_holder_num | {ok/fail} | {time18} | — |
| stock_locked_shares | {ok/fail} | {time19} | — |
| stock_pledge_ratio | {ok/fail} | {time20} | — |
| stock_top10_holders | {ok/fail} | {time21} | — |
| stock_valuation_compare | {ok/fail} | {time22} | 估值与行业对比 |
| stock_dividend_history | {ok/fail} | {time23} | 分红历史 |
| stock_financial_compare | {ok/fail} | {time24} | 财务指标详情 |
| stock_market_pe_percentile | {ok/fail} | {time25} | 市场PE分位 |
| stock_industry_pe | {ok/fail} | {time26} | 行业PE对比 |
| stock_institutional_holdings | {ok/fail} | {time27} | 基金重仓股 |
| stock_earnings_calendar | {ok/fail} | {time28} | 财报日历 |
| trading_signals | {ok/fail} | {time29} | 交易信号 |
| stock_screener | {ok/fail} | {time30} | 选股器 |
| backtest_strategy | {ok/fail} | {time31} | 策略回测 |
| portfolio_risk_analysis | {ok/fail} | {time32} | 组合风险 |

### 港股工具测试

| 工具 | 状态 | 耗时(s) | 备注 |
|------|------|--------|------|
| stock_info | {ok/fail} | {time1} | {note1} |
| stock_prices | {ok/fail} | {time2} | {note2} |
| stock_indicators | {ok/fail} | {time3} | {note3} |

### 美股工具测试

| 工具 | 状态 | 耗时(s) | 备注 |
|------|------|--------|------|
| stock_prices | {ok/fail} | {time1} | {note1} |
| stock_indicators | {ok/fail} | {time2} | {note2} |
| stock_overview_us | {ok/fail} | {time3} | {note3} |
| stock_financials_us | {ok/fail} | {time4} | {note4} |
| stock_earnings_us | {ok/fail} | {time5} | {note5} |
| stock_insider_us | {ok/fail} | {time6} | {note6} |

### 加密货币工具测试

| 工具 | 状态 | 耗时(s) | 备注 |
|------|------|--------|------|
| okx_prices | {ok/fail} | {time1} | {note1} |
| okx_loan_ratios | {ok/fail} | {time2} | {note2} |
| okx_taker_volume | {ok/fail} | {time3} | {note3} |
| binance_ai_report | {ok/fail} | {time4} | {note4} |

### 通用工具测试

| 工具 | 状态 | 耗时(s) | 备注 |
|------|------|--------|------|
| get_current_time | {ok/fail} | {time1} | {note1} |
| stock_news | {ok/fail} | {time2} | {note2} |
| stock_news_global | {ok/fail} | {time3} | {note3} |

---

### 测试汇总

| 指标 | 数值 |
|------|------|
| 总计工具数 | {total} |
| 成功数 | {success} |
| 失败数 | {failed} |
| 成功率(%) | {rate} |

### 失败项详情

| 工具 | 市场 | 错误信息 |
|------|------|---------|
| {tool1} | {market1} | {error1} |
| {tool2} | {market2} | {error2} |
```
