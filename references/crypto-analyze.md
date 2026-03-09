# 加密货币综合分析

根据用户提供的币种进行全面分析。默认分析 BTC，支持 ETH、SOL 等主流币种。

### 分析流程

1. `okx_prices` (bar=1D, limit=60) - 获取日线K线数据和技术指标
2. `okx_prices` (bar=4H, limit=50) - 获取4小时K线观察短期趋势
3. `okx_loan_ratios` (period=1H) - 获取杠杆多空比
4. `okx_loan_ratios` (period=1D) - 获取日线多空比趋势
5. `okx_taker_volume` (instType=SPOT, period=1H) - 获取现货主动买卖
6. `okx_taker_volume` (instType=CONTRACTS, period=1H) - 获取衍生品主动买卖
7. `binance_ai_report` - 获取币安AI分析报告
8. `stock_news` (symbol=币种) - 获取相关新闻
9. 根据以上数据综合分析，给出投资建议

### instId 格式
币种传入时自动补全: BTC → BTC-USDT, ETH → ETH-USDT

### 输出格式

使用 Markdown 格式输出，便于阅读：

```markdown
## {币种}-USDT 综合分析报告

### 价格走势

| 周期 | 当前价格 | 涨跌幅(%) | 趋势 |
|------|---------|----------|------|
| 24H | {price} | {change_24h} | {trend_24h} |
| 7D | {price} | {change_7d} | {trend_7d} |
| 日线 | {price} | — | {daily_trend} |
| 4H | {price} | — | {4h_trend} |

### 技术指标

| 指标 | 日线值 | 4H值 | 信号 |
|------|-------|------|------|
| MACD | {macd_d} | {macd_4h} | {signal} |
| RSI14 | {rsi_d} | {rsi_4h} | {signal} |
| KDJ | K={k} D={d} J={j} | {kdj_4h} | {signal} |
| 布林带 | {boll_pos_d} | {boll_pos_4h} | {signal} |
| OBV | {obv_trend_d} | {obv_trend_4h} | {signal} |

### 市场情绪

| 指标 | 数值 | 判断 |
|------|------|------|
| 多空比 | {loan_ratio} | {bias} |
| 现货买卖比 | 买入{buy_pct}%/卖出{sell_pct}% | {spot_sentiment} |
| 衍生品买卖比 | 买入{buy_pct}%/卖出{sell_pct}% | {contract_sentiment} |
| 综合情绪 | — | {overall_sentiment} |

### AI分析（币安）

| 类型 | 内容 |
|------|------|
| 概述 | {overview} |
| 观点 | {point1} |
| 观点 | {point2} |

### 投资建议

| 操作 | 置信度 | 理由 | 风险提示 |
|------|--------|------|---------|
| {action} | {confidence} | {reason} | {risk} |
```
