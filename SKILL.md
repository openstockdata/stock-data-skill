---
name: stock-data
description: "股票/加密货币数据分析。分析A股/港股/美股行情、技术指标、财务数据、资金流向、筹码分布，加密货币K线和多空比，市场全景，板块轮动，持仓组合评估。"
argument-hint: <股票代码或分析指令>
homepage: https://github.com/openstockdata/stock-data-skill
metadata:
  openclaw:
    requires:
      bins: ["stock-data"]
      env: ["TUSHARE_TOKEN", "ALPHA_VANTAGE_API_KEY"]
    primaryEnv: TUSHARE_TOKEN
    emoji: "📈"
    tags: [stock, crypto, analysis, financial-data, akshare]
---

## 工具调用方式

所有数据工具通过 `stock-data` CLI 直接调用:

```bash
stock-data <tool_name> key=value key2=value2
```

输出为 CSV 格式文本（`#` 开头为元数据注释行），直接解析即可。可并行调用多个独立命令。

### 常用示例

```bash
stock-data stock_realtime symbol=600519 market=sh
stock-data stock_prices symbol=300058 market=sz limit=60
stock-data search keyword=茅台
stock-data stock_indicators symbol=600519 market=sh
stock-data stock_chip symbol=300058
stock-data stock_fund_flow symbol=300058
stock-data trading_signals symbol=300058 days=60
stock-data okx_prices instId=BTC-USDT bar=1D limit=60
stock-data stock_news_global
stock-data stock_batch_realtime symbols=600519,000858,601318
stock-data --list    # 查看全部可用工具
```

## 分析流程

根据用户意图，读取对应参考文档获取详细分析流程：

| 用户意图 | 参考文档 | 典型触发词 |
|---------|---------|-----------|
| 分析单只股票 | `references/stock-analyze.md` | "分析茅台"、"看看600519"、"AAPL怎么样" |
| 分析加密货币 | `references/crypto-analyze.md` | "分析BTC"、"比特币走势"、"ETH行情" |
| 市场全景概览 | `references/market-overview.md` | "市场概览"、"今日大盘"、"A股行情" |
| 持仓组合分析 | `references/portfolio-analyze.md` | "分析持仓"、"我的股票"、多个股票代码 |
| 板块轮动分析 | `references/sector-analyze.md` | "分析人工智能板块"、"银行板块" |
| 数据源健康检查 | `references/stock-health-check.md` | "健康检查"、"数据源状态" |

## 市场识别规则

- 6位纯数字 → A股（0/3开头=sz，6开头=sh）
- 5位数字 → 港股 (hk)
- 纯英文字母 → 美股 (us)
- 加密货币符号（BTC、ETH等） → 自动补全为 BTC-USDT 格式

## 输出格式约定

- **工具返回数据**：CSV 格式，`#` 开头行为元数据
- **分析报告**（面向用户）：Markdown 格式，含表格、标题、强调

## 完整工具列表

参见 `references/tools.md` 获取全部 47 个工具的参数说明。
