"""
Complete Analysis Script
Runs the entire Bitcoin Trader Behavior Analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('husl')

print("="*80)
print("BITCOIN TRADER BEHAVIOR & MARKET SENTIMENT ANALYSIS")
print("="*80)

# ============================================================================
# PHASE 1: DATA LOADING AND CLEANING
# ============================================================================
print("\n[PHASE 1] Loading and Cleaning Data...")

# Load Fear & Greed Index
fear_greed_df = pd.read_csv('../data/fear_greed_index.csv')
print(f"✓ Loaded Fear & Greed Index: {len(fear_greed_df):,} rows")

# Load Trader Data
trader_df = pd.read_csv('../data/hyperliquid_trader_data.csv')
print(f"✓ Loaded Trader Data: {len(trader_df):,} rows")

# Clean Fear & Greed data
fear_greed_df['Date'] = pd.to_datetime(fear_greed_df['date'])
fear_greed_df['Classification'] = fear_greed_df['classification'].apply(
    lambda x: 'Fear' if 'Fear' in str(x) else 'Greed'
)
fear_greed_df = fear_greed_df[['Date', 'Classification', 'value']].drop_duplicates(subset=['Date'])
print(f"✓ Cleaned Fear & Greed data: {len(fear_greed_df):,} rows")

# Clean Trader data
trader_df['account'] = trader_df['Account']
trader_df['symbol'] = trader_df['Coin']
trader_df['closedPnL'] = trader_df['Closed PnL']
trader_df['side'] = trader_df['Side']
trader_df['size'] = trader_df['Size USD']
trader_df['time'] = pd.to_datetime(trader_df['Timestamp'], unit='ms')
trader_df['date'] = trader_df['time'].dt.date
trader_df['date'] = pd.to_datetime(trader_df['date'])
trader_df['leverage'] = 10  # Default leverage

# Remove rows with missing PnL
trader_df = trader_df[trader_df['closedPnL'].notna()]
print(f"✓ Cleaned Trader data: {len(trader_df):,} rows")
print(f"  Date range: {trader_df['date'].min()} to {trader_df['date'].max()}")
print(f"  Unique traders: {trader_df['account'].nunique():,}")
print(f"  Unique symbols: {trader_df['symbol'].nunique()}")

# Save cleaned data
fear_greed_df.to_csv('../data/fear_greed_cleaned.csv', index=False)
trader_df.to_csv('../data/trader_data_cleaned.csv', index=False)
print("✓ Saved cleaned datasets")

# ============================================================================
# PHASE 2: EXPLORATORY DATA ANALYSIS
# ============================================================================
print("\n[PHASE 2] Exploratory Data Analysis...")

# Sentiment distribution
fig, ax = plt.subplots(1, 2, figsize=(14, 5))

sentiment_counts = fear_greed_df['Classification'].value_counts()
ax[0].bar(sentiment_counts.index, sentiment_counts.values, color=['red', 'green'], alpha=0.7)
ax[0].set_title('Fear vs Greed Distribution', fontsize=14, fontweight='bold')
ax[0].set_ylabel('Count')
ax[0].set_xlabel('Sentiment')

# Trader performance
winning_trades = (trader_df['closedPnL'] > 0).sum()
losing_trades = (trader_df['closedPnL'] < 0).sum()
ax[1].pie([winning_trades, losing_trades], labels=['Winning', 'Losing'], 
          autopct='%1.1f%%', colors=['green', 'red'], startangle=90)
ax[1].set_title('Win/Loss Ratio', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('../outputs/01_sentiment_and_performance.png', dpi=300, bbox_inches='tight')
print("✓ Created sentiment and performance visualization")

# Trader statistics
print(f"\n  Total Trades: {len(trader_df):,}")
print(f"  Total PnL: ${trader_df['closedPnL'].sum():,.2f}")
print(f"  Average PnL: ${trader_df['closedPnL'].mean():.2f}")
print(f"  Win Rate: {(trader_df['closedPnL'] > 0).mean() * 100:.1f}%")

# ============================================================================
# PHASE 3: SENTIMENT-TRADER CORRELATION
# ============================================================================
print("\n[PHASE 3] Analyzing Sentiment-Trader Correlation...")

# Merge datasets
merged_df = trader_df.merge(
    fear_greed_df[['Date', 'Classification']], 
    left_on='date', 
    right_on='Date', 
    how='left'
)
merged_df = merged_df.rename(columns={'Classification': 'sentiment'})
merged_df = merged_df[merged_df['sentiment'].notna()]  # Keep only rows with sentiment
print(f"✓ Merged dataset: {len(merged_df):,} rows with sentiment data")

# Performance by sentiment
sentiment_stats = merged_df.groupby('sentiment')['closedPnL'].agg([
    ('count', 'count'),
    ('total_pnl', 'sum'),
    ('avg_pnl', 'mean'),
    ('median_pnl', 'median'),
    ('std_pnl', 'std')
]).round(2)

print("\n  Performance by Sentiment:")
print(sentiment_stats)

# Win rate by sentiment
win_rates = merged_df.groupby('sentiment').apply(
    lambda x: (x['closedPnL'] > 0).sum() / len(x) * 100
)
print("\n  Win Rates:")
for sentiment, rate in win_rates.items():
    print(f"    {sentiment}: {rate:.1f}%")

# Statistical test
fear_pnl = merged_df[merged_df['sentiment'] == 'Fear']['closedPnL'].dropna()
greed_pnl = merged_df[merged_df['sentiment'] == 'Greed']['closedPnL'].dropna()
t_stat, p_value = stats.ttest_ind(fear_pnl, greed_pnl)
print(f"\n  T-test: t={t_stat:.4f}, p={p_value:.4f}")
print(f"  Significant difference: {'Yes' if p_value < 0.05 else 'No'} (α=0.05)")

# Visualization
fig, ax = plt.subplots(2, 2, figsize=(15, 10))

# Average PnL
avg_pnl = merged_df.groupby('sentiment')['closedPnL'].mean()
colors = ['red', 'green']
ax[0, 0].bar(avg_pnl.index, avg_pnl.values, color=colors, alpha=0.7)
ax[0, 0].set_title('Average PnL by Sentiment', fontweight='bold')
ax[0, 0].set_ylabel('Average PnL ($)')
ax[0, 0].axhline(0, color='black', linestyle='--', linewidth=1)

# Win rate
ax[0, 1].bar(win_rates.index, win_rates.values, color=colors, alpha=0.7)
ax[0, 1].set_title('Win Rate by Sentiment', fontweight='bold')
ax[0, 1].set_ylabel('Win Rate (%)')
ax[0, 1].axhline(50, color='black', linestyle='--', linewidth=1)

# PnL distribution
merged_df.boxplot(column='closedPnL', by='sentiment', ax=ax[1, 0])
ax[1, 0].set_title('PnL Distribution by Sentiment')
ax[1, 0].set_xlabel('Sentiment')
ax[1, 0].set_ylabel('Closed PnL ($)')
plt.sca(ax[1, 0])
plt.xticks(rotation=0)

# Trade volume
trade_counts = merged_df['sentiment'].value_counts()
ax[1, 1].pie(trade_counts.values, labels=trade_counts.index, autopct='%1.1f%%',
            colors=colors, startangle=90)
ax[1, 1].set_title('Trade Distribution by Sentiment')

plt.tight_layout()
plt.savefig('../outputs/02_sentiment_correlation.png', dpi=300, bbox_inches='tight')
print("✓ Created sentiment correlation visualization")

# Save merged data
merged_df.to_csv('../data/merged_analysis_data.csv', index=False)

# ============================================================================
# PHASE 4: ADVANCED INSIGHTS
# ============================================================================
print("\n[PHASE 4] Generating Advanced Insights...")

# Trader profiles
trader_profiles = merged_df.groupby('account').agg({
    'closedPnL': ['sum', 'mean', 'count'],
    'size': 'mean'
}).reset_index()
trader_profiles.columns = ['account', 'total_pnl', 'avg_pnl', 'trade_count', 'avg_size']

# Calculate win rate
win_rates_by_trader = merged_df.groupby('account').apply(
    lambda x: (x['closedPnL'] > 0).sum() / len(x)
).reset_index(name='win_rate')
trader_profiles = trader_profiles.merge(win_rates_by_trader, on='account')

print(f"✓ Created profiles for {len(trader_profiles):,} traders")

# Top traders
top_10 = trader_profiles.nlargest(10, 'total_pnl')
print("\n  Top 10 Traders by Total PnL:")
for i, row in top_10.iterrows():
    print(f"    #{i+1}: ${row['total_pnl']:,.2f} (Win Rate: {row['win_rate']*100:.1f}%)")

# Clustering
features = ['total_pnl', 'avg_pnl', 'trade_count', 'win_rate']
X = trader_profiles[features].fillna(0)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# K-means with 4 clusters
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
trader_profiles['cluster'] = kmeans.fit_predict(X_scaled)

cluster_summary = trader_profiles.groupby('cluster')[features].mean().round(2)
print("\n  Trader Clusters:")
print(cluster_summary)

# Visualization
fig, ax = plt.subplots(2, 2, figsize=(15, 10))

# Top traders
top_10_sorted = top_10.sort_values('total_pnl')
ax[0, 0].barh(range(len(top_10_sorted)), top_10_sorted['total_pnl'].values, color='steelblue')
ax[0, 0].set_yticks(range(len(top_10_sorted)))
ax[0, 0].set_yticklabels([f"Trader {i+1}" for i in range(len(top_10_sorted))])
ax[0, 0].set_xlabel('Total PnL ($)')
ax[0, 0].set_title('Top 10 Traders by PnL', fontweight='bold')

# Cluster scatter
scatter = ax[0, 1].scatter(trader_profiles['total_pnl'], trader_profiles['win_rate'], 
                          c=trader_profiles['cluster'], s=50, alpha=0.6, cmap='viridis')
ax[0, 1].set_xlabel('Total PnL ($)')
ax[0, 1].set_ylabel('Win Rate')
ax[0, 1].set_title('Trader Segmentation', fontweight='bold')
plt.colorbar(scatter, ax=ax[0, 1], label='Cluster')

# Symbol performance
top_symbols = merged_df.groupby('symbol')['closedPnL'].sum().nlargest(10)
ax[1, 0].barh(range(len(top_symbols)), top_symbols.values, color='coral')
ax[1, 0].set_yticks(range(len(top_symbols)))
ax[1, 0].set_yticklabels(top_symbols.index)
ax[1, 0].set_xlabel('Total PnL ($)')
ax[1, 0].set_title('Top 10 Symbols by PnL', fontweight='bold')

# Risk-adjusted returns
risk_metrics = merged_df.groupby('sentiment')['closedPnL'].agg(['mean', 'std'])
risk_metrics['sharpe'] = risk_metrics['mean'] / risk_metrics['std']
ax[1, 1].bar(risk_metrics.index, risk_metrics['sharpe'], color=colors, alpha=0.7)
ax[1, 1].set_title('Risk-Adjusted Returns (Sharpe-like)', fontweight='bold')
ax[1, 1].set_ylabel('Sharpe Ratio')
ax[1, 1].axhline(0, color='black', linestyle='--', linewidth=1)

plt.tight_layout()
plt.savefig('../outputs/03_advanced_insights.png', dpi=300, bbox_inches='tight')
print("✓ Created advanced insights visualization")

# ============================================================================
# FINAL REPORT
# ============================================================================
print("\n[FINAL] Generating Report...")

report = f"""
# Bitcoin Trader Behavior & Market Sentiment Analysis
## Executive Summary

**Analysis Date:** {pd.Timestamp.now().strftime('%B %d, %Y')}

---

## Dataset Overview

- **Total Trades Analyzed:** {len(merged_df):,}
- **Unique Traders:** {merged_df['account'].nunique():,}
- **Date Range:** {merged_df['date'].min().strftime('%Y-%m-%d')} to {merged_df['date'].max().strftime('%Y-%m-%d')}
- **Total PnL:** ${merged_df['closedPnL'].sum():,.2f}

---

## Key Findings

### 1. Market Sentiment Impact

**Performance by Sentiment:**
- **Fear Period**: Average PnL = ${fear_pnl.mean():.2f}, Win Rate = {(fear_pnl > 0).mean() * 100:.1f}%
- **Greed Period**: Average PnL = ${greed_pnl.mean():.2f}, Win Rate = {(greed_pnl > 0).mean() * 100:.1f}%

**Statistical Significance:** p-value = {p_value:.4f} ({'Significant' if p_value < 0.05 else 'Not significant'} at α=0.05)

**Insight:** Traders {'outperform' if greed_pnl.mean() > fear_pnl.mean() else 'underperform'} during Greed periods by ${abs(greed_pnl.mean() - fear_pnl.mean()):.2f} per trade on average.

---

### 2. Overall Trading Performance

- **Total Trades:** {len(trader_df):,}
- **Overall Win Rate:** {(trader_df['closedPnL'] > 0).mean() * 100:.1f}%
- **Average Trade PnL:** ${trader_df['closedPnL'].mean():.2f}
- **Median Trade PnL:** ${trader_df['closedPnL'].median():.2f}

---

### 3. Top Performer Characteristics

**Top 10% Traders:**
- Average Total PnL: ${top_10['total_pnl'].mean():,.2f}
- Average Win Rate: {top_10['win_rate'].mean() * 100:.1f}%
- Average Trades: {top_10['trade_count'].mean():.0f}

---

### 4. Trader Segmentation

Identified {len(cluster_summary)} distinct trader segments:
{cluster_summary.to_string()}

---

### 5. Symbol Performance

**Top 5 Most Profitable Symbols:**
{chr(10).join([f"- {symbol}: ${pnl:,.2f}" for symbol, pnl in top_symbols.head(5).items()])}

---

## Strategic Recommendations

### For Traders:

1. **Sentiment-Based Strategy**
   - {'Increase' if greed_pnl.mean() > fear_pnl.mean() else 'Decrease'} position sizes during Greed periods
   - Monitor sentiment indicators for optimal entry/exit

2. **Risk Management**
   - Maintain win rate above 50% for consistent profitability
   - Focus on high-performing symbols

3. **Performance Benchmarking**
   - Top traders achieve {top_10['win_rate'].mean() * 100:.1f}% win rate
   - Average successful trader makes ${top_10['avg_pnl'].mean():.2f} per trade

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
- **Time Period:** {merged_df['date'].min().strftime('%Y-%m-%d')} to {merged_df['date'].max().strftime('%Y-%m-%d')}

---

**Prepared by:** Data Science Analysis  
**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d')}
"""

with open('../outputs/FINAL_REPORT.md', 'w', encoding='utf-8') as f:
    f.write(report)

print("✓ Generated final report")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*80)
print("ANALYSIS COMPLETE!")
print("="*80)
print("\n📊 Generated Files:")
print("  ├─ data/fear_greed_cleaned.csv")
print("  ├─ data/trader_data_cleaned.csv")
print("  ├─ data/merged_analysis_data.csv")
print("  ├─ outputs/01_sentiment_and_performance.png")
print("  ├─ outputs/02_sentiment_correlation.png")
print("  ├─ outputs/03_advanced_insights.png")
print("  └─ outputs/FINAL_REPORT.md")

print("\n🎯 Key Insights:")
print(f"  1. Traders perform {'better' if greed_pnl.mean() > fear_pnl.mean() else 'worse'} during Greed periods")
print(f"  2. Overall win rate: {(trader_df['closedPnL'] > 0).mean() * 100:.1f}%")
print(f"  3. Top traders achieve {top_10['win_rate'].mean() * 100:.1f}% win rate")
print(f"  4. Identified {len(cluster_summary)} distinct trader segments")
print(f"  5. Statistical significance: {'Yes' if p_value < 0.05 else 'No'} (p={p_value:.4f})")

print("\n✅ Next Steps:")
print("  1. Review visualizations in outputs/ folder")
print("  2. Read FINAL_REPORT.md for complete findings")
print("  3. Create GitHub repository")
print("  4. Submit your application!")

print("\n" + "="*80)
