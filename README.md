# Luxury Brands Trends Tracker

Automated monitoring of luxury brand search interest in China and globally using Google Trends.

![Dashboard Preview](https://img.shields.io/badge/Status-Active-success)
![Updates](https://img.shields.io/badge/Updates-Daily-blue)
![Cost](https://img.shields.io/badge/Cost-Free-green)

## 📊 What This Tracks

**Brands:**
- Louis Vuitton
- Dior
- Hermès
- Gucci
- Cartier

**Regions:**
- China (mainland) - Primary focus
- Global - For comparison

**Metrics:**
- Search interest index (0-100)
- 7-day trends
- 12-month historical data
- China vs Global correlation signals

## 🎯 Use Case

Built for LVMH stock analysis - tracking real-time consumer interest in luxury brands as a potential leading indicator for:
- Quarterly earnings performance
- Regional demand shifts (especially China)
- Brand health monitoring
- Competitive positioning

## 🔄 How It Works

1. **Daily Automation:** GitHub Actions runs `fetch_trends.py` every day at 3:00 AM UTC
2. **Data Collection:** Script queries Google Trends API for all brands in both regions
3. **Storage:** Results saved to `trends_data.json` in this repository
4. **Visualization:** Dashboard reads the JSON and renders interactive charts

## 📁 Files

- `fetch_trends.py` - Main data collection script
- `dashboard_with_trends.html` - Interactive dashboard
- `.github/workflows/update-trends.yml` - Automation configuration
- `trends_data.json` - Auto-generated data file (updated daily)

## 🚀 Quick Start

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions.

**TL;DR:**
1. Fork this repo
2. Enable GitHub Actions with write permissions
3. Update dashboard URL with your username
4. Access your dashboard via GitHub Pages

## 📈 Dashboard Features

### KPI Cards
Current search interest with 7-day change indicators for each brand

### Trend Charts
- Interactive line charts
- Toggle between 7-day and 12-month views
- Separate charts for China and Global

### Signal Analysis
Automated correlation between China and Global trends:
- ✓ **Strong Buy** - Both markets rising
- ⚠️ **Mixed** - Regional divergence  
- ✗ **Weak** - Both markets declining

## 🔧 Customization

### Add More Brands

Edit `fetch_trends.py`:
```python
BRANDS = {
    'newbrand': {'en': 'English Name', 'cn': '中文名'},
}
```

### Change Update Frequency

Edit `.github/workflows/update-trends.yml`:
```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
```

## 📊 Data Format

`trends_data.json` structure:
```json
{
  "metadata": {
    "last_update": "2026-04-08T03:00:00",
    "brands": ["lv", "dior", "hermes", "cartier", "gucci"],
    "regions": ["china", "global"]
  },
  "china": {
    "7d": {
      "labels": ["2026-04-01", "2026-04-02", ...],
      "datasets": {
        "LV": [45, 48, 52, ...],
        "迪奥": [38, 42, 41, ...]
      },
      "latest": {
        "LV": { "value": 52, "change": 8.5 }
      }
    },
    "12m": { ... }
  },
  "global": { ... }
}
```

## 🔒 Privacy & Costs

- ✅ **100% Free** - Uses GitHub's free tier
- ✅ **No API Keys** - Google Trends is publicly accessible
- ✅ **No Personal Data** - Only aggregated search trends
- ✅ **Open Source** - Fully transparent methodology

## 📝 License

MIT License - Feel free to use and modify

## 🙏 Attribution

Powered by:
- [pytrends](https://github.com/GeneralMills/pytrends) - Google Trends API wrapper
- [Chart.js](https://www.chartjs.org/) - Dashboard charts
- GitHub Actions - Free automation

## ⚠️ Disclaimer

This tool provides search trend data only. It is not financial advice. Always conduct thorough research before making investment decisions.

---

**Last Update:** Auto-updated by GitHub Actions
