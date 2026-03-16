# 单票股票综合分析（工程执行手册）

> 目标：对用户给定的单个标的（A股/港股/美股/ETF）做一次结构化分析，输出 **Markdown 报告**并落盘到 `./stock-reports/`，支持与上次报告对比。

---

## 0. 输入与标准化

### 0.1 输入
- 代码或名称：`600036` / `09988` / `AAPL` / `招商银行`
- 可选：成本价、数量（仅用于展示；**不得**用于交易建议推导）

### 0.2 市场识别（market）
- 6位纯数字且 `0/3` 开头 → A股深圳 `sz`
- 6位纯数字且 `6` 开头 → A股上海 `sh`
- 5位数字 → 港股 `hk`
- 纯英文字母 → 美股 `us`

### 0.3 ETF 识别（is_etf，仅A股）
- 代码以 `51/15/16` 开头 → ETF

### 0.4 代码确认（必要时）
- 若用户给的是名称/模糊代码：先 `search` 确认唯一 `symbol`。

---

## 1. 全局硬约束（必须遵守）

### 1.1 成本价/收益率
- 成本价允许为负数。
- 当成本价为负数或接近 0：收益率失真 → **不展示/不引用**。
- **禁止**基于盈亏%做止盈止损/加减仓理由。
- 建议只能基于：技术面/资金面/基本面/行业与估值等客观信号。

### 1.2 交易日/盘中/收盘声明
分析前**必须**调用 `get_current_time`：
- 非交易日：声明“交易数据基于上一交易日({日期})，资讯为当日({日期})”。
- 盘中：声明“盘中实时数据，收盘前可能变化”。
- 已收盘：声明“当日收盘数据”。

### 1.3 ETF 特殊处理（A股）
- ETF **禁止**调用：`stock_chip`、`stock_fund_flow`、`stock_top10_holders`、`stock_holder_num` 等个股结构工具。
- ETF 重点：跟踪指数、成交量、技术指标（折溢价如可得）。

---

## 2. 执行流程（MVP 优先，Optional 按需）

### Step 0：历史报告对比准备（分析前执行）
- Glob：`./stock-reports/{market}-{symbol}-*.md`，找到最近的**非当日**报告并读取（如有）。
- 暂存上次关键要点：上次建议、上次价格（如能从文本抽取）、关键指标信号摘要。

### Step 1：基础信息与行情（必做）
1) `get_current_time`
2) `stock_info`（按 market；若工具要求则带 market）
3) `stock_prices`（market/period=daily, limit=60）
4) `stock_realtime`（若该市场支持；用于盘中/收盘标注与当日波动）
5) `stock_indicators`（market=sh/sz/hk/us）

> 注：`stock_prices` 已含常用技术指标（MA/MACD/KDJ/RSI/BOLL/ADX/CCI/WR/VWAP/OBV/ATR 等）。不需要在文档里重复解释每个指标的定义，只需在结论里引用“触发的信号”。

### Step 2：分市场增强项

#### 2.1 A股（非ETF）
**MVP（必调）**
1) `stock_fund_flow`
2) `stock_sector_spot`
3) `stock_period_stats`
4) `stock_valuation_compare`
5) `trading_signals`（days=60）

**Optional（按需触发）**
- 筹码判断需要时：`stock_chip`
- 股东结构需要时：`stock_top10_holders`（holder_type=circulate）
- 筹码集中/散户化判断：`stock_holder_num`
- 高股息策略：`stock_dividend_history`
- 杠杆情绪：`stock_margin_trading`
- 解禁检查：`stock_locked_shares`（mode=detail）
- 深度财务拆解：`stock_financial_compare`
- 新闻核对：`stock_news`（limit=5）

#### 2.2 A股（ETF）
**必调**
1) `stock_sector_spot`（若能返回指数/赛道信息则用；否则可省略）
2) `stock_period_stats`
3) `trading_signals`（若适用/可得）

#### 2.3 港股
1) `stock_news`（limit=5）

#### 2.4 美股
1) `stock_overview_us`
2) `stock_earnings_us`
3) `stock_financials_us`（report_type=income_statement）
4) `stock_insider_us`
5) `stock_news_us`（可选）

---

## 3. 输出要求（硬格式）

### 3.1 报告骨架（必须包含）
- 数据声明（交易日/盘中/收盘/上一交易日）
- 基本面摘要（行业/市值/估值/ROE/成长）
- 技术面摘要（趋势/动能/超买超卖/波动/量能的关键信号）
- 资金/结构（仅A股个股，且仅在调用后输出）
- 结论与建议（加仓/持有/减仓/观望）
- 风险提示（至少 3 条，且与数据对应）

### 3.2 Markdown 模板（推荐）

```markdown
## {name} ({market}-{symbol}) 综合分析报告
> 生成时间: {time} | 数据说明: {盘中/收盘/上一交易日}

### 一句话结论
{一句话总结：趋势 + 关键风险 + 建议}

### 基本面（摘要）
- 行业/赛道：{...}
- 市值：{...}
- 估值：{PE/PB 及行业相对}
- 盈利与成长：{ROE/营收/净利增速要点}

### 技术面（关键信号）
- 趋势：{价格相对 MA20/MA60；是否多头排列}
- 动能：{MACD/KDJ/RSI 的 1-2 个核心信号}
- 波动：{BOLL/ATR 体现的收敛/扩张}
- 量能：{成交量/VWAP/OBV 是否配合}

### 资金与结构（仅A股个股）
- 主力净流入：{...}
- 结构：{超大单/大单占比变化}
- 筹码（如有）：{获利盘/成本区/集中度}
- 股东（如有）：{十大流通/股东人数趋势要点}

### 结论与建议
- 建议：{加仓/持有/减仓/观望}
- 置信度：{高/中/低}
- 依据（列 3-5 条）：
  1) {指标→信号→结论}
  2) ...

### 风险提示
- {风险1：来自某指标/事件/结构}
- {风险2}
- {风险3}
```

---

## 4. 落盘与历史对比（必须）

### 4.1 写文件
- 目录：`./stock-reports/`（不存在则创建）
- 文件名：`{market}-{symbol}-{YYYYMMDD}.md`（如 `sh-600036-20260226.md`）
- 同日同股多次分析：覆盖同日文件

### 4.2 追加对比章节（如有历史报告）
在报告末尾追加：

```markdown
---

### 与上次分析对比（{上次日期} → {本次日期}）
- 建议变化：{上次→本次}（原因：...）
- 价格区间变化（如可得）：{...}
- 关键技术信号变化：{MACD/KDJ/RSI/ADX 要点}
- 资金/结构变化（如有）：{主力/筹码/股东}
```

无历史报告：注明“首次分析，无历史对比”。
