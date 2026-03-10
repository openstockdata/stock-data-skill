# 股票综合分析

根据用户提供的股票进行全面分析。自动判断市场类型：
- 6位纯数字 → A股（0/3开头=sz，6开头=sh）
- 5位数字 → 港股 (hk)
- 英文字母 → 美股 (us)

### A股分析流程
1. `search` - 确认股票代码
2. `stock_info` - 获取基本信息
3. `stock_prices` (period=daily, limit=60) - 获取日线数据+技术指标（含ADX/CCI/WR/VWAP）
4. `stock_realtime` - 获取实时行情
5. `stock_indicators` (market=sh/sz) - 获取财务指标
6. `stock_chip` - 获取筹码分布
7. `stock_fund_flow` - 获取资金流向
8. `stock_sector_spot` - 获取所属板块
9. `stock_period_stats` - 获取多周期统计
10. `stock_valuation_compare` - 获取估值与行业对比（PE/PB分位数）
11. `stock_top10_holders` (symbol, holder_type=circulate) - 获取十大流通股东变化
12. `trading_signals` (symbol, days=60) - 获取技术面交易信号（MACD/KDJ/RSI综合评分）
13. `stock_dividend_history` (symbol, limit=10) - 获取分红历史和股息率（可选）
14. `stock_financial_compare` (symbol) - 获取详细财务指标（盈利/成长/偿债/运营）
15. `stock_north_flow` - 获取北向资金流向（可选）
16. `stock_margin_trading` (symbol) - 获取融资融券数据（可选）
17. `stock_holder_num` (symbol) - 获取股东人数变化（可选）
18. `stock_locked_shares` (mode=detail) - 查询该股是否有近期解禁（可选）
19. `stock_news` - 获取相关新闻（可选）
20. 根据以上数据综合分析，给出投资建议

### 港股分析流程
1. `stock_info` (market=hk) - 获取基本信息
2. `stock_prices` (market=hk, limit=60) - 获取日线数据+技术指标
3. `stock_indicators` (market=hk) - 获取财务指标
4. `stock_news` - 获取相关新闻
5. 根据以上数据综合分析，给出投资建议

### 美股分析流程
1. `stock_overview_us` - 获取公司概览（市值、PE、EPS、分析师评级）
2. `stock_prices` (market=us, limit=60) - 获取日线数据+技术指标
3. `stock_indicators` (market=us) - 获取财务指标
4. `stock_financials_us` (report_type=income_statement) - 获取利润表
5. `stock_earnings_us` - 获取盈利数据
6. `stock_insider_us` - 获取内部交易
7. `stock_news_us` - 获取美股新闻（可选）
8. 根据以上数据综合分析，给出投资建议

### 重要规则约束

#### 1. 成本价与收益率
- 如果用户提供了成本价，成本价可能为负数（多次交易后已收回成本），此时收益率失真，不应基于收益率给出止盈/止损建议
- 操作建议必须基于技术面、资金面、基本面的客观数据信号

#### 2. 非交易日分析
- 分析前调用 `get_current_time` 确认交易日状态
- 非交易日分析需声明"交易数据基于上一交易日，新闻资讯为当日"
- 盘中分析注明"数据为盘中实时，收盘前可能变化"

#### 3. ETF 特殊处理
- ETF（代码以51/15/16开头）不调用 `stock_chip`、`stock_fund_flow`、`stock_top10_holders` 等个股专属工具
- ETF 重点关注：跟踪指数、折溢价、成交量、技术指标

### 技术指标说明

stock_prices 工具返回的技术指标包括：
- **趋势指标**: MA5/MA10/MA20/MA30/MA60, ADX（趋势强度）, +DI/-DI（多空方向）
- **动量指标**: MACD(DIF/DEA), RSI(6/12/14/24), KDJ(K/D/J), CCI, Williams %R
- **波动指标**: BOLL(上/中/下轨), BOLL.W（布林带宽度，波动率收缩/扩张）, ATR
- **量能指标**: OBV, VWAP（成交量加权均价）, VMA5/VMA10（成交量均线）

### 输出格式

使用 Markdown 格式输出，便于阅读：

```markdown
## {股票名称} ({代码}) 综合分析报告

### 基本面

| 指标 | 数值 |
|------|------|
| 行业 | {行业} |
| 市值(亿) | {市值} |
| 市盈率 | {PE} |
| 市净率 | {PB} |
| ROE(%) | {ROE} |

### 估值分析（A股）

| 指标 | 个股值 | 行业中位数 | 分位数(%) | 估值水平 |
|------|--------|-----------|----------|---------|
| PE | {pe} | {median_pe} | {pct} | {level} |
| PB | {pb} | {median_pb} | {pct} | {level} |

### 技术面

| 指标 | 数值 | 信号 |
|------|------|------|
| 均线系统 | {ma_desc} | {trend} |
| 趋势强度ADX | {adx} | {adx_signal} |
| MACD | {macd} | {macd_signal} |
| KDJ | K={k} D={d} J={j} | {kdj_signal} |
| RSI14 | {rsi} | {rsi_signal} |
| CCI | {cci} | {cci_signal} |
| WR | {wr} | {wr_signal} |
| 布林带 | {boll_pos} | {boll_signal} |
| VWAP | {vwap} | {vwap_vs_price} |

### 资金面（A股）

| 类型 | 金额(万) | 占比(%) | 趋势 |
|------|---------|---------|------|
| 主力 | {main_flow} | {pct} | {trend} |
| 超大单 | {xl_flow} | {pct} | {trend} |
| 大单 | {l_flow} | {pct} | {trend} |

### 筹码分布（A股）

| 获利比例(%) | 平均成本 | 90%成本区间 | 集中度 | 筹码状态 |
|------------|---------|-----------|-------|---------|
| {profit_ratio} | {avg_cost} | {cost_90_low}-{cost_90_high} | {concentration} | {chip_status} |

### 股东结构（A股）

| 十大流通股东变化 | 机构持仓 | 解禁风险 |
|----------------|---------|---------|
| {holder_change} | {institution} | {unlock_risk} |

### 交易信号（A股）

| 多头得分 | 空头得分 | 综合得分 | 信号 |
|---------|---------|---------|------|
| {buy_score} | {sell_score} | {total_score} | {signal} |

### 财务趋势（A股）

| 指标 | 变化 | 数值 | 评价 |
|------|------|------|------|
| ROE变化 | {roe_trend} | {roe_change} | — |
| 净利润增速 | — | {profit_growth} | {growth_level} |
| 资产负债率 | — | {debt_ratio} | {risk_level} |

### 分红情况（A股）

| 最近派息(元/10股) | 股息率(%) | 评价 |
|------------------|---------|------|
| {dividend} | {yield} | {dividend_eval} |

### 投资建议

| 操作 | 置信度 | 理由 | 风险提示 |
|------|--------|------|---------|
| {action} | {confidence} | {reason} | {risk} |
```

### 报告持久化与历史对比

#### 报告文件管理

每次分析完成后，**必须**将完整报告写入文件：

1. **目录**: `~/stock-reports/`（不存在则创建）
2. **文件名**: `{market}-{symbol}-{YYYYMMDD}.md`，如 `hk-09988-20260226.md`、`sh-600036-20260226.md`、`us-AAPL-20260226.md`
3. **同一天多次分析同一只股票**: 直接覆盖同日文件（以最新分析为准）

```bash
# 文件路径示例
~/stock-reports/hk-09988-20260226.md
~/stock-reports/sh-600036-20260226.md
~/stock-reports/us-AAPL-20260226.md
```

#### 历史报告对比流程

**在开始分析前**，先查找该股票的上次分析报告：

1. **查找上次报告**: 用 Glob 搜索 `~/stock-reports/{market}-{symbol}-*.md`，找到日期最近的非当日文件
2. **读取上次报告**: 如果找到，读取该文件内容，暂存关键数据（价格、建议、指标评分等）
3. **执行本次分析**: 按正常流程完成全部分析
4. **生成对比章节**: 在报告末尾追加"与上次分析对比"章节：

```markdown
---

### 与上次分析对比（{上次日期} → {本次日期}）

#### 价格变化
| 上次价格 | 本次价格 | 区间涨跌(%) | 区间天数 |
|---------|---------|-----------|---------|
| {prev_price} | {curr_price} | {change_pct} | {days} |

#### 关键指标变化
| 指标 | 上次 | 本次 | 变化趋势 |
|------|------|------|---------|
| MACD | {prev_macd} | {curr_macd} | {trend} |
| KDJ | {prev_kdj} | {curr_kdj} | {trend} |
| RSI14 | {prev_rsi} | {curr_rsi} | {trend} |
| ADX | {prev_adx} | {curr_adx} | {trend} |
| 资金流向 | {prev_flow} | {curr_flow} | {trend} |
| 筹码获利比 | {prev_chip} | {curr_chip} | {trend} |

#### 建议变化
| 上次建议 | 本次建议 | 变化原因 |
|---------|---------|---------|
| {prev_action} | {curr_action} | {reason} |

#### 上次建议回顾
- 上次建议: {prev_recommendation}
- 如果按上次建议操作的结果: {retrospective}
- 建议准确度评估: {accuracy_note}
```

5. **写入文件**: 将完整报告（含对比章节）写入当日文件
6. **无历史报告时**: 跳过对比，仅写入当次报告，并在文件末尾注明"首次分析，无历史对比"

#### 报告写入步骤（在分析完成后执行）

```
1. mkdir -p ~/stock-reports/
2. Glob 查找 ~/stock-reports/{market}-{symbol}-*.md（分析开始前执行）
3. 如果找到非当日历史文件 → 读取最近一份 → 暂存关键数据
4. 完成本次分析 → 生成对比章节
5. Write 完整报告到 ~/stock-reports/{market}-{symbol}-{YYYYMMDD}.md
6. 告知用户报告已保存的路径及与上次的关键变化

