# 市场全景分析

提供A股市场的全面概览，帮助判断市场整体趋势和情绪。

### 分析流程

#### 第一步：基础信息
1. `get_current_time` - 获取当前时间和交易日状态
2. `stock_news_global` - 获取全球财经快讯

#### 第二步：指数行情
1. `stock_batch_realtime` (symbols=000001,399001,399006,000300,000905) - 获取主要指数
   - 000001: 上证指数
   - 399001: 深证成指
   - 399006: 创业板指
   - 000300: 沪深300
   - 000905: 中证500

#### 第三步：资金流向
1. `stock_north_flow` (indicator=北向资金) - 北向资金流向
2. `stock_margin_trading` (market=sh, limit=10) - 沪市融资融券
3. `stock_margin_trading` (market=sz, limit=10) - 深市融资融券
4. `stock_sector_fund_flow_rank` (days=今日, cate=行业资金流) - 行业资金流向

#### 第四步：市场热点
1. `stock_zt_pool` (pool_type=涨停, limit=30) - 涨停股池
2. `stock_zt_pool` (pool_type=跌停, limit=20) - 跌停股池
3. `stock_lhb_ggtj_sina` (days=5, limit=20) - 龙虎榜统计

#### 第五步：市场风险指标
1. `stock_locked_shares` (mode=summary, limit=10) - 近期解禁压力
2. `stock_pledge_ratio` (mode=market, limit=10) - 市场整体质押水平

#### 第六步：市场估值
1. `stock_market_pe_percentile` - 市场PE历史分位
2. `stock_industry_pe` - 各行业PE对比（发现低估/高估行业）

#### 第七步：机构动向与事件
1. `stock_institutional_holdings` (limit=20) - 基金重仓股变化（了解机构最新持仓方向）
2. `stock_earnings_calendar` (limit=20) - 即将披露财报的公司（财报季关注）
3. `stock_screener` (pe_max=20, pb_max=2, change_min=0, limit=10) - 低估值上涨股筛选（可选）

### 分析维度

#### 指数趋势
- **上证指数**: 主板市场风向标
- **创业板指**: 成长股情绪指标
- **沪深300**: 权重股表现
- **中证500**: 中盘股表现

#### 资金面
- **北向资金**: 外资动向，市场风向标
- **融资余额**: 杠杆资金情绪
- **板块资金**: 热点方向

#### 市场情绪
- **涨跌比**: 上涨/下跌家数
- **涨停数**: 市场强度
- **跌停数**: 恐慌程度
- **龙虎榜**: 机构/游资动向

#### 估值水平
- **PE分位**: 历史估值位置
- **行业PE对比**: 低估/高估行业识别
- **情绪判断**: 贪婪/恐惧

#### 机构动向
- **基金重仓变化**: 增仓/减仓/新进方向
- **财报披露**: 近期财报事件

#### 供给压力
- **限售解禁**: 近期解禁规模和节奏
- **股权质押**: 市场整体质押比例趋势

### 输出格式

使用 Markdown 格式输出，便于阅读：

```markdown
## A股市场全景
> 生成时间: {当前时间} | 交易状态: {交易中/已收盘/休市}

### 指数行情

| 指数 | 最新 | 涨跌(%) | 成交额(亿) |
|------|------|---------|----------|
| 上证指数 | {price1} | {change1} | {amount1} |
| 深证成指 | {price2} | {change2} | {amount2} |
| 创业板指 | {price3} | {change3} | {amount3} |
| 沪深300 | {price4} | {change4} | {amount4} |
| 中证500 | {price5} | {change5} | {amount5} |

### 北向资金

| 指标 | 数值 |
|------|------|
| 今日净流入(亿) | {today_flow} |
| 近5日累计(亿) | {5d_flow} |
| 资金动向 | {flow_trend} |

### 融资融券

| 市场 | 融资余额(亿) | 较昨日(亿) | 杠杆情绪 |
|------|------------|----------|---------|
| 沪市 | {sh_balance} | {sh_change} | {sh_sentiment} |
| 深市 | {sz_balance} | {sz_change} | {sz_sentiment} |

### 板块资金 Top5

| 板块 | 净流入(亿) | 涨跌(%) |
|------|----------|---------|
| {sector1} | {flow1} | {change1} |
| {sector2} | {flow2} | {change2} |
| {sector3} | {flow3} | {change3} |
| {sector4} | {flow4} | {change4} |
| {sector5} | {flow5} | {change5} |

### 涨跌分布

| 类型 | 数量 | 占比(%) |
|------|------|--------|
| 上涨 | {up_count} | {up_pct} |
| 下跌 | {down_count} | {down_pct} |
| 涨停 | {zt_count} | — |
| 跌停 | {dt_count} | — |

### 涨停分析

| 类型 | 内容 |
|------|------|
| 连板股 | {multi_board_stocks} |
| 首板数量 | {first_board_count} |
| 涨停题材 | {zt_themes} |

### 龙虎榜活跃

| 股票 | 上榜次数 | 买入额(万) | 卖出额(万) |
|------|---------|----------|----------|
| {stock1} | {count1} | {buy1} | {sell1} |
| {stock2} | {count2} | {buy2} | {sell2} |

### 市场估值

| 指标 | 数值 |
|------|------|
| 当前PE分位(%) | {pe_pct} |
| 历史位置 | {pe_level} |
| 估值状态 | {valuation} |

**行业估值对比**

| 类型 | 行业 |
|------|------|
| 低估值行业 | {low_pe_sectors} |
| 高估值行业 | {high_pe_sectors} |

### 基金重仓变化

| 股票 | 基金数 | 持仓变化 | 市值(亿) |
|------|-------|---------|---------|
| {stock1} | {count1} | {change1} | {value1} |
| {stock2} | {count2} | {change2} | {value2} |

### 限售解禁

| 周期 | 解禁市值(亿) |
|------|------------|
| 本周 | {this_week} |
| 下周 | {next_week} |
| 高冲击个股 | {high_impact_stocks} |

### 股权质押

| 指标 | 数值 |
|------|------|
| 当前质押比例(%) | {pledge_ratio} |
| 趋势 | {pledge_trend} |
| 高质押行业 | {high_pledge_sectors} |

---

### 综合研判

| 类型 | 内容 |
|------|------|
| 市场状态 | {market_state} |
| 短期趋势 | {short_trend} |
| 判断依据 | {basis} |
| 仓位建议 | {position} |
| 关注方向 | {focus_sectors} |
| 风险提示 | {risk_warning} |
```
