# 持仓组合综合分析

批量分析用户提供的股票持仓，充分利用 stock-data-mcp 提供的全部工具。

### 支持的输入格式

1. **代码列表**: `600036,000651,09988,AAPL`
2. **持仓表格**: 包含代码、名称、成本价、持仓数量的表格

### 市场识别规则

- 6位数字0/3开头 → A股深圳 (sz)
- 6位数字6开头 → A股上海 (sh)
- 5位数字 → 港股 (hk)
- 纯英文字母 → 美股 (us)

### 分析流程

#### 第一步：市场概览（先调用）
1. `get_current_time` - 获取当前时间和交易日状态
2. `stock_news_global` - 获取全球财经快讯
3. `stock_sector_fund_flow_rank` (days=今日, cate=行业资金流) - 获取板块资金流向
4. `stock_zt_pool` (pool_type=涨停, limit=20) - 获取涨停股池了解市场热点
5. `stock_lhb_ggtj_sina` (days=5, limit=20) - 获取龙虎榜数据
6. `stock_north_flow` - 获取北向资金流向

#### 第二步：A股持仓分析（每只股票调用）
对每只A股，调用以下工具：
1. `stock_realtime` (symbol, market) - 实时行情（价格、涨跌、量比、换手）
2. `stock_prices` (symbol, market, limit=60) - 日K线+技术指标（MA/MACD/KDJ/RSI/BOLL/ADX/CCI/WR/VWAP）
3. `stock_fund_flow` (symbol) - 资金流向（主力/超大单/大单/中单/小单）
4. `stock_chip` (symbol) - 筹码分布（获利比例、平均成本、集中度）
5. `stock_indicators` (symbol, market) - 财务指标（PE/PB/ROE/营收增长）
6. `stock_sector_spot` (symbol) - 所属板块（行业+概念）
7. `stock_period_stats` (symbol, market) - 多周期统计（5/10/20/60日涨跌幅）
8. `stock_valuation_compare` (symbol) - 估值与行业对比（PE/PB分位数）
9. `stock_top10_holders` (symbol, holder_type=circulate) - 十大流通股东变化
10. `trading_signals` (symbol, days=60) - 技术面交易信号（综合评分）
11. `stock_financial_compare` (symbol) - 详细财务指标（盈利/成长/偿债/运营）
12. `stock_dividend_history` (symbol) - 分红历史和股息率（可选，适合高股息策略）
13. `stock_margin_trading` (symbol) - 融资融券数据（可选）
14. `stock_holder_num` (symbol) - 股东人数变化（可选）

**批量优化**: 如果持仓超过5只A股，先用 `stock_batch_realtime` 批量获取实时行情

#### 第二步补充：组合级风险检查
1. `stock_locked_shares` (mode=detail, limit=100) - 检查持仓中是否有近期解禁股票
2. `stock_pledge_ratio` (mode=industry) - 了解持仓所在行业的质押风险
3. `portfolio_risk_analysis` (symbols=持仓代码列表, days=60) - 组合风险指标（波动率/回撤/相关性/夏普比率）
4. `stock_institutional_holdings` (limit=30) - 查看基金重仓股变化（了解机构动向）

#### 第三步：港股持仓分析（每只股票调用）
1. `stock_realtime` (symbol, market=hk) - 实时行情
2. `stock_prices` (symbol, market=hk, limit=60) - 日K线+技术指标
3. `stock_indicators` (symbol, market=hk) - 财务指标
4. `stock_news` (symbol, limit=5) - 相关新闻

#### 第四步：美股持仓分析（每只股票调用）
1. `stock_prices` (symbol, market=us, limit=60) - 日K线+技术指标
2. `stock_overview_us` (symbol) - 公司概览（市值、PE、52周高低、分析师评级）
3. `stock_indicators` (symbol, market=us) - 财务指标
4. `stock_earnings_us` (symbol) - 盈利数据

### 重要规则约束

#### 1. 成本价与收益率处理
- **成本价可以为负数**：用户多次交易后可能已收回全部成本甚至盈利，此时成本价为负值，这是正常的
- **收益率失真**：当成本价为负数或接近零时，计算出的收益率（盈亏%）无意义，不应展示或参考
- **禁止基于收益率推荐操作**：买入/持有/减仓建议必须基于技术面、资金面、基本面信号，不得基于"已盈利xx%应该止盈"或"已亏损xx%应该止损"
- **持仓汇总中**：对负成本的股票，盈亏%列显示"-"，不计算百分比

#### 2. 非交易日分析
- 分析前必须调用 `get_current_time` 确认当前是否为交易日
- **非交易日**（周末/节假日）：报告开头必须明确声明"本次分析交易数据基于上一交易日({日期})，新闻资讯为当日({日期})"
- **盘中分析**：注明"数据为盘中实时数据，收盘前可能变化"
- **已收盘**：注明"数据为当日收盘数据"

#### 3. ETF 与个股区分
- **ETF**（代码以51/15/16开头）：不调用 `stock_chip`、`stock_fund_flow`、`stock_top10_holders`、`stock_holder_num` 等个股专属工具
- **ETF 分析重点**：跟踪指数表现、折溢价、成交量、技术指标
- **个股分析重点**：全维度分析（技术面+资金面+基本面+股东结构）

#### 4. 操作建议原则
- 建议必须基于客观数据信号（技术指标、资金流向、估值水平、行业趋势）
- 不使用用户的持仓成本和盈亏比例作为买卖依据
- 对同一行业/概念过度集中的持仓给出风险提示
- 明确说明建议依据的具体指标和数据

### 分析维度

对每只股票，从以下维度分析：

#### 技术面
- **趋势**: 价格 vs MA5/10/20/60 位置
- **趋势强度**: ADX 数值（>25强趋势，<20弱趋势）
- **动能**: MACD 金叉/死叉，柱状图方向
- **超买超卖**: KDJ 位置，RSI 水平，CCI，Williams %R
- **波动**: 布林带位置，ATR 幅度
- **量能**: OBV 趋势，成交量变化，VWAP 位置

#### 资金面（A股专属）
- **主力动向**: 主力净流入/流出
- **筹码结构**: 获利盘比例，套牢盘压力
- **集中度**: 筹码集中度90%/70%
- **北向资金**: 外资流向
- **融资融券**: 杠杆资金动向
- **股东人数**: 筹码集中趋势

#### 股东结构（A股专属）
- **十大流通股东**: 机构/基金新进或退出
- **持仓变化**: 增持/减持趋势
- **解禁压力**: 近期是否有限售解禁
- **质押风险**: 所属行业质押水平

#### 基本面
- **估值**: PE/PB/PS 与行业对比
- **盈利**: ROE、净利润增速
- **成长**: 营收增速、EPS增长

#### 板块联动（A股专属）
- **行业**: 所属行业及行业排名
- **概念**: 热门概念题材
- **资金流**: 板块资金动向

### 输出格式

使用 Markdown 格式输出，便于阅读：

```markdown
## 持仓组合分析报告
> 生成时间: {当前时间} | 市场状态: {交易日/休市}

### 市场概览

**热点板块 Top5**

| 板块 | 涨跌幅(%) | 主力净流入(亿) | 代表股 |
|------|----------|--------------|-------|
| {板块1} | {change1} | {flow1} | {stock1} |
| {板块2} | {change2} | {flow2} | {stock2} |

**龙虎榜活跃**

| 股票 | 上榜次数 | 买入额(万) | 卖出额(万) |
|------|---------|----------|----------|
| {stock1} | {count1} | {buy1} | {sell1} |

---

### 持仓汇总

| 代码 | 名称 | 现价 | 涨跌(%) | 成本 | 盈亏(%) | 仓位(%) |
|------|------|------|---------|------|---------|--------|
| {code1} | {name1} | {price1} | {change1} | {cost1} | {pnl1} | {weight1} |

**今日盈亏**: {daily_pnl}元 | **持仓市值**: {total_value}元

---

### 个股分析: {股票名称} ({代码})

**实时行情**

| 现价 | 涨跌(%) | 成交量(万手) | 成交额(亿) | 换手率(%) | 量比 |
|------|---------|------------|----------|----------|------|
| {price} | {change} | {volume} | {amount} | {turnover} | {vol_ratio} |

**技术面评分: {score}/100**

| 指标 | 数值 | 信号 |
|------|------|------|
| MA趋势 | {ma_desc} | {ma_signal} |
| MACD | DIF={dif} DEA={dea} | {macd_signal} |
| KDJ | K={k} D={d} J={j} | {kdj_signal} |
| RSI14 | {rsi} | {rsi_signal} |
| ADX | {adx} | {adx_signal} |
| 布林带 | {boll_pos} | {boll_signal} |

**资金面评分: {score}/100**（A股）

| 类型 | 金额(万) | 占比(%) | 趋势 |
|------|---------|---------|------|
| 主力 | {main_flow} | {main_pct} | {main_trend} |
| 超大单 | {xl_flow} | {xl_pct} | {xl_trend} |

**筹码分布**（A股）

| 获利比例(%) | 平均成本 | 90%成本区间 | 集中度 | 状态 |
|------------|---------|-----------|-------|------|
| {profit_ratio} | {avg_cost} | {cost_90} | {conc} | {chip_status} |

**财务面评分: {score}/100**

| PE(TTM) | PB | ROE(%) | 营收增速(%) | 净利润增速(%) |
|---------|-----|--------|-----------|-------------|
| {pe} | {pb} | {roe} | {rev_growth} | {profit_growth} |

**综合评级**

| 技术面 | 资金面 | 基本面 | 总评分 | 操作建议 | 理由 |
|--------|-------|-------|-------|---------|------|
| {tech_stars} | {fund_stars} | {fund_stars} | {total_score} | {action} | {reason} |

---

### 交易信号汇总

| 代码 | 名称 | 多头得分 | 空头得分 | 信号 | 建议 |
|------|------|---------|---------|------|------|
| {code1} | {name1} | {buy1} | {sell1} | {signal1} | {action1} |

---

### 组合风险分析

| 预期年化收益(%) | 年化波动率(%) | 夏普比率 | 最大回撤(%) |
|---------------|-------------|---------|-----------|
| {portfolio_return} | {portfolio_vol} | {sharpe} | {max_dd} |

**相关性风险**

| 高相关性对 | 相关系数 |
|-----------|---------|
| {pair1} | {corr1} |

---

### 风险提示

| 风险类型 | 详情 |
|---------|------|
| 高风险持仓 | {high_risk_stocks} |
| 止损预警 | {stop_loss_warning} |
| 板块集中风险 | {sector_concentration} |
| 解禁压力 | {unlock_pressure} |

---

### 操作建议汇总

| 操作 | 股票 | 理由 |
|------|------|------|
| **加仓** | {stocks_to_add} | {add_reason} |
| **持有** | {stocks_to_hold} | {hold_reason} |
| **减仓** | {stocks_to_reduce} | {reduce_reason} |
| **观望** | {stocks_to_watch} | {watch_reason} |
```

### 报告持久化与历史对比

#### 报告文件管理

每次分析完成后，**必须**将完整报告写入文件：

1. **目录**: `~/stock-reports/`（不存在则创建）
2. **文件名**: `portfolio-report-{YYYYMMDD}.md`，如 `portfolio-report-20260225.md`
3. **同一天多次分析**: 直接覆盖同日文件（以最新分析为准）

```bash
# 文件路径示例
~/stock-reports/portfolio-report-20260225.md
~/stock-reports/portfolio-report-20260226.md
```

#### 历史报告对比流程

在完成当次分析后，执行以下对比步骤：

1. **查找上次报告**: 用 Glob 搜索 `~/stock-reports/portfolio-report-*.md`，找到日期最近的非当日文件
2. **读取上次报告**: 读取该文件内容
3. **生成对比章节**: 在报告末尾追加"与上次分析对比"章节，包含：

```markdown
---

### 与上次分析对比（{上次日期} → {本次日期}）

#### 持仓变动
| 代码 | 名称 | 上次建议 | 本次建议 | 变化原因 |
|------|------|---------|---------|---------|
| {code} | {name} | {prev_action} | {curr_action} | {reason} |

#### 市场环境变化
| 维度 | 上次 | 本次 | 变化 |
|------|------|------|------|
| 热点板块 | {prev_sectors} | {curr_sectors} | {change} |
| 北向资金 | {prev_north} | {curr_north} | {change} |
| 市场情绪 | {prev_sentiment} | {curr_sentiment} | {change} |

#### 关键指标变化
| 代码 | 名称 | 上次价格 | 现价 | 区间涨跌(%) | 建议变化 |
|------|------|---------|------|-----------|---------|
| {code} | {name} | {prev_price} | {curr_price} | {change_pct} | {action_change} |

#### 上次建议执行回顾
- 上次建议加仓的股票表现: {performance_summary}
- 上次建议减仓的股票表现: {performance_summary}
- 建议准确度评估: {accuracy_note}
```

4. **写入文件**: 将完整报告（含对比章节）写入当日文件
5. **无历史报告时**: 跳过对比，仅写入当次报告，并在文件末尾注明"首次分析，无历史对比"

#### 报告写入步骤（在分析完成后执行）

```
1. mkdir -p ~/stock-reports/
2. Glob 查找 ~/stock-reports/portfolio-report-*.md
3. 如果找到非当日历史文件 → 读取最近一份 → 生成对比章节
4. Write 完整报告到 ~/stock-reports/portfolio-report-{YYYYMMDD}.md
5. 告知用户报告已保存的路径
```
