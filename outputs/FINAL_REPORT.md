
# Bitcoin Trader Behavior & Market Sentiment Analysis
## Executive Summary

**Analysis Date:** November 22, 2025

---

## Dataset Overview

- **Total Trades Analyzed:** 184,263
- **Unique Traders:** 32
- **Date Range:** 2023-03-28 to 2025-02-19
- **Total PnL:** $10,225,249.60

---

## Key Findings

### 1. Market Sentiment Impact

**Performance by Sentiment:**
- **Fear Period**: Average PnL = $50.05, Win Rate = 41.5%
- **Greed Period**: Average PnL = $69.96, Win Rate = 43.4%

**Statistical Significance:** p-value = 0.0000 (Significant at α=0.05)

**Insight:** Traders outperform during Greed periods by $19.91 per trade on average.

---

### 2. Overall Trading Performance

- **Total Trades:** 211,224
- **Overall Win Rate:** 41.1%
- **Average Trade PnL:** $48.75
- **Median Trade PnL:** $0.00

---

### 3. Top Performer Characteristics

**Top 10% Traders:**
- Average Total PnL: $806,801.48
- Average Win Rate: 46.1%
- Average Trades: 9858

---

### 4. Trader Segmentation

Identified 4 distinct trader segments:
          total_pnl  avg_pnl  trade_count  win_rate
cluster                                            
0         265144.55   159.98      2705.43      0.56
1         108763.42    30.46      4805.44      0.37
2        1264087.54    69.40     24044.67      0.41
3         654808.41   401.36      1673.25      0.33

---

### 5. Symbol Performance

**Top 5 Most Profitable Symbols:**
- @107: $2,776,897.53
- HYPE: $1,911,331.06
- ETH: $1,431,097.42
- SOL: $1,371,096.31
- BTC: $659,311.31

---

## Strategic Recommendations

### For Traders:

1. **Sentiment-Based Strategy**
   - Increase position sizes during Greed periods
   - Monitor sentiment indicators for optimal entry/exit

2. **Risk Management**
   - Maintain win rate above 50% for consistent profitability
   - Focus on high-performing symbols

3. **Performance Benchmarking**
   - Top traders achieve 46.1% win rate
   - Average successful trader makes $195.99 per trade

---

## Visualizations

All charts saved in `outputs/` directory:
1. `01_sentiment_and_performance.png` - Sentiment distribution and win/loss ratio
2. `02_sentiment_correlation.png` - Performance analysis by sentiment
3. `03_advanced_insights.png` - Top traders, clustering, and risk metrics

---

## Methodology

- **Data Sources:** Fear & Greed Index + Hyperliquid trader data
- **Analysis Techniques:** Descriptive statistics, t-tests, K-means clustering
- **Time Period:** 2023-03-28 to 2025-02-19

---

**Prepared by:** Data Science Analysis  
**Date:** 2025-11-22
