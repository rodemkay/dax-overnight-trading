# DAX Overnight Trading System - the_don EA

## 🚀 Overview
Professional automated trading system for DAX index overnight trading using MetaTrader 5.

### Current Version: **the_don v1.25 FINAL CLEAN**
- **License Code:** DERDON
- **Program Name:** the_don  
- **Status:** Production Ready
- **Release Date:** 29.08.2025

## 📁 Project Structure
```
dax-overnight-trading/
├── src/
│   ├── EA/                    # MetaTrader 5 Expert Advisors
│   │   └── the_don.mq5        # Main EA (Active Development)
│   ├── Include/               # MQL Include Files
│   └── Scripts/               # Python automation scripts
├── docs/                      # Documentation
├── backtest/                  # Backtest results
├── config/                    # Configuration files
└── README.md
```

## 🔧 Features
- **Multi-Symbol Support** - Works with any trading symbol
- **Advanced Filters:**
  - ATR Filter (Volatility)
  - StochRSI Filter (H4 Timeframe)
  - Gap Filter
  - RSI/ADX/MACD Filters
- **Risk Management:**
  - Trailing Stop
  - Night Protection
  - Max Daily Loss Protection
- **License System:**
  - Server-based verification
  - RoboForex Affiliate integration
  - Demo protection with time limits
- **Performance Display** - Real-time symbol performance in chart

## 💻 System Requirements
- MetaTrader 5 Terminal
- Windows 11 (for MetaEditor compilation)
- Linux Server (for automation scripts)
- Python 3.x for scripts
- Active internet connection for license verification

## 🔐 License System
Three-tier hierarchy:
1. **RoboForex Affiliate** → Unlimited usage
2. **Server License** → Duration controlled by server
3. **Demo Mode** → Time-limited trial

## 📊 Trading Parameters
### Main Settings
- **MagicNumber:** 10124689 (default)
- **Lot Size:** 0.10 (customizable)
- **Stop Loss:** 50 points
- **Take Profit:** 500 points
- **Trading Hours:** 22:00 - 08:45 (DAX overnight)

### Filter Settings (Internal)
- **StochRSI:** Always enabled (H4)
- **ATR Filter:** Disabled by default (minATR=100)
- **Other filters:** User configurable

## 🛠️ Installation

### 1. MetaTrader Setup
```bash
# Copy EA to MetaTrader
cp src/EA/the_don.mq5 /path/to/MT5/MQL5/Experts/
```

### 2. Compile in MetaEditor
- Open MetaEditor
- Load the_don.mq5
- Press F7 to compile

### 3. Configure in MT5
- Attach to DAX chart (or any symbol)
- Set your preferred parameters
- Enable auto-trading

## 🔄 Development Workflow

### Version Control
```bash
# Clone repository
git clone [repository-url]

# Create feature branch
git checkout -b feature/new-feature

# Commit changes
git add .
git commit -m "Add new feature"

# Push to GitHub
git push origin feature/new-feature
```

### Testing
1. Backtest in Strategy Tester
2. Forward test on demo account
3. Deploy to production

## 📝 Changelog
See [CHANGELOG.md](CHANGELOG_2025-08-12.md) for detailed version history.

## 🤝 Support
- **Website:** www.forexsignale.trade/daxovernight
- **License:** https://lic.prophelper.org

## ⚠️ Risk Disclaimer
Trading forex and CFDs involves significant risk and can result in the loss of your invested capital. Past performance is not indicative of future results.

## 📜 License
Proprietary software - All rights reserved.

---
*Last updated: August 13, 2025*