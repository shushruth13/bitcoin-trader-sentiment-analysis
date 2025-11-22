# Bitcoin Trader Behavior & Market Sentiment Analysis

> Analyzing the relationship between Bitcoin market sentiment (Fear/Greed Index) and trader performance on Hyperliquid

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Complete-success.svg)]()

---

## 📊 Executive Summary

This analysis examines **184,263 trades** from **32 traders** across **246 symbols** to uncover the relationship between market sentiment and trading performance.

**Key Finding:** Traders perform **40% better during Greed periods** ($69.96 vs $50.05 avg PnL, p < 0.0001)

---

## 🔍 Key Insights

### 1. Sentiment Impact (Statistically Significant)
- **Greed Period:** $69.96 avg PnL, 43.4% win rate
- **Fear Period:** $50.05 avg PnL, 41.5% win rate
- **Difference:** $19.91 per trade advantage
- **P-value:** < 0.0001 (highly significant)

### 2. Trader Segmentation (4 Clusters)
- **High-Skill Traders:** 56% win rate, $160 avg PnL
- **Volume Traders:** 37% win rate, 4,805 avg trades
- **Mega Traders:** 41% win rate, 24,044 avg trades
- **High-Value Traders:** 33% win rate, $401 avg PnL

### 3. Symbol Performance
Top 5 symbols account for **80% of total profits** ($8.15M):
- @107: $2.78M
- HYPE: $1.91M
- ETH: $1.43M
- SOL: $1.37M
- BTC: $659K

### 4. Top Trader Characteristics
- Average Total PnL: $806,801
- Average Win Rate: 46.1%
- Best Performer: 80.9% win rate

---

## 📁 Project Structure

```
├── data/                          # Datasets
│   ├── fear_greed_index.csv      # Original sentiment data
│   ├── hyperliquid_trader_data.csv # Original trader data
│   ├── fear_greed_cleaned.csv    # Cleaned sentiment data
│   ├── trader_data_cleaned.csv   # Cleaned trader data
│   └── merged_analysis_data.csv  # Combined dataset
│
├── outputs/                       # Results
│   ├── 01_sentiment_and_performance.png
│   ├── 02_sentiment_correlation.png
│   ├── 03_advanced_insights.png
│   └── FINAL_REPORT.md
│
├── src/                          # Analysis code
│   └── run_complete_analysis.py  # Main analysis script
│
├── .gitignore
├── requirements.txt
├── README.md
├── ANALYSIS_COMPLETE.md          # Detailed findings
└── SUBMISSION_TEMPLATE.txt       # Email template
```

---

## 🚀 Quick Start

### Run the Analysis

```bash
# Install dependencies
pip install -r requirements.txt

# Run complete analysis
cd src
python run_complete_analysis.py
```

The script will:
1. Load and clean both datasets
2. Perform exploratory data analysis
3. Analyze sentiment-trader correlations
4. Generate trader segmentation
5. Create visualizations
6. Generate final report

---

## 📈 Methodology

### Data Sources
- **Fear & Greed Index:** 2,644 daily sentiment readings
- **Hyperliquid Trader Data:** 211,224 trade executions

### Analysis Techniques
- **Statistical Testing:** Independent t-tests for significance
- **Machine Learning:** K-means clustering for trader segmentation
- **Risk Analysis:** Sharpe-like ratios for risk-adjusted returns
- **Visualization:** Professional charts using Matplotlib/Seaborn

### Time Period
March 28, 2023 - February 19, 2025 (23 months)

---

## 💡 Strategic Recommendations

### For Traders
1. **Increase position sizes during Greed periods** (40% better performance)
2. **Focus on top 5 symbols** (@107, HYPE, ETH, SOL, BTC)
3. **Target 46%+ win rate** to match top performers
4. **Monitor sentiment indicators** for optimal entry/exit

### For Platform
1. **Implement sentiment-based alerts** for users
2. **Provide trader benchmarking** against segments
3. **Offer symbol performance analytics**
4. **Develop risk management education**

---

## 🛠️ Technologies Used

- **Python 3.11**
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Matplotlib/Seaborn** - Visualizations
- **Scikit-learn** - Machine learning
- **SciPy** - Statistical testing

---

## 📊 Results

All visualizations and detailed findings available in:
- `outputs/FINAL_REPORT.md` - Complete analysis report
- `ANALYSIS_COMPLETE.md` - Detailed insights and recommendations

---

## 👤 Author

**Shushruth Gowda MB**  
📧 shushruth1344@gmail.com  
🔗 [LinkedIn](http://linkedin.com/in/shushruthgowdamb)  
💻 [GitHub](http://github.com/shushruth13)

---

## 📝 License

This project is for educational and portfolio purposes.

---

## 🙏 Acknowledgments

- Prime Trade for the assignment opportunity
- Hyperliquid for trader data
- Bitcoin Fear & Greed Index data providers

---

**⭐ If you find this analysis insightful, please star the repository!**
