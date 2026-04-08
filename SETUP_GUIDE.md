# Google Trends Dashboard - Setup Guide

## 🎯 What You're Building

An automated dashboard that tracks luxury brand search interest in China and globally, updating daily without manual intervention.

**Tech Stack:**
- Python script (fetches Google Trends data)
- GitHub Actions (runs automatically every day at 3 AM UTC)
- HTML Dashboard (reads data from GitHub)
- **Cost: $0 (completely free)**

---

## 📋 Prerequisites

1. **GitHub Account** (free) - [Sign up here](https://github.com/signup)
2. **Python installed** (to test locally first)
   - Windows: Download from [python.org](https://www.python.org/downloads/)
   - Mac: Already installed or use `brew install python`
   - Linux: `sudo apt install python3 python3-pip`

---

## 🚀 Step-by-Step Setup

### STEP 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and log in
2. Click the **"+"** icon (top right) → **"New repository"**
3. Repository settings:
   - Name: `luxury-trends-tracker` (or any name you want)
   - Description: `Automated luxury brand trends monitoring`
   - **Make it PUBLIC** (required for free GitHub Actions)
   - ✅ Check "Add a README file"
4. Click **"Create repository"**

### STEP 2: Upload Files to GitHub

You have 3 files to upload:

**Method A - Web Upload (Easiest):**

1. In your new repo, click **"Add file"** → **"Upload files"**
2. Drag these 3 files:
   - `fetch_trends.py`
   - `dashboard_with_trends.html`
   - `.github/workflows/update-trends.yml` (you'll need to create the folder structure)

**Method B - Git Command Line:**

```bash
# Clone your repo
git clone https://github.com/YOUR-USERNAME/luxury-trends-tracker.git
cd luxury-trends-tracker

# Copy the 3 files here

# Create workflow directory
mkdir -p .github/workflows

# Move files to correct locations
# - fetch_trends.py (root)
# - dashboard_with_trends.html (root)
# - update-trends.yml (inside .github/workflows/)

# Commit and push
git add .
git commit -m "Initial setup: trends tracker"
git push
```

### STEP 3: Configure GitHub Actions

1. In your GitHub repo, go to **"Settings"** → **"Actions"** → **"General"**
2. Under **"Workflow permissions"**:
   - Select ✅ **"Read and write permissions"**
   - Click **"Save"**

This allows the GitHub Action to commit updated data back to your repo.

### STEP 4: Enable GitHub Actions

1. Go to the **"Actions"** tab in your repo
2. You should see the workflow **"Update Google Trends Data"**
3. Click on it
4. Click **"Enable workflow"** (if needed)

### STEP 5: Run First Test

**Option 1 - Manual trigger:**
1. In **Actions** tab → Select your workflow
2. Click **"Run workflow"** → **"Run workflow"**
3. Wait 1-2 minutes
4. Check if `trends_data.json` appears in your repo

**Option 2 - Wait for scheduled run:**
- It will run automatically at 3:00 AM UTC daily
- First run happens tomorrow at 3 AM

### STEP 6: Update Dashboard URL

1. Open `dashboard_with_trends.html` in a text editor
2. Find line ~218:
   ```javascript
   const response = await fetch('https://raw.githubusercontent.com/YOUR-USERNAME/YOUR-REPO/main/trends_data.json');
   ```
3. Replace with:
   ```javascript
   const response = await fetch('https://raw.githubusercontent.com/YOUR-USERNAME/luxury-trends-tracker/main/trends_data.json');
   ```
   (Use your actual GitHub username)

4. Save and commit this change

### STEP 7: Access Your Dashboard

**Option A - GitHub Pages (Recommended):**

1. In your repo, go to **Settings** → **Pages**
2. Under "Source", select **"main"** branch
3. Click **"Save"**
4. Wait 1-2 minutes
5. Your dashboard will be at:
   ```
   https://YOUR-USERNAME.github.io/luxury-trends-tracker/dashboard_with_trends.html
   ```

**Option B - Local viewing:**

1. Download `dashboard_with_trends.html` to your computer
2. Open it in Chrome/Firefox
3. The dashboard will fetch data from GitHub automatically

---

## 🔧 How It Works

### Daily Automation Flow

```
Every day at 3:00 AM UTC:
1. GitHub Actions wakes up
2. Runs fetch_trends.py
3. Script queries Google Trends API
4. Downloads last 7 days + 12 months data
5. For China (geo='CN') and Global
6. Saves to trends_data.json
7. Commits file back to GitHub
8. Your dashboard reads the updated JSON
```

### What Gets Tracked

**Brands:**
- Louis Vuitton (LV / Louis Vuitton)
- Dior (迪奥 / Dior)
- Hermès (爱马仕 / Hermès)
- Gucci (Gucci / Gucci)
- Cartier (卡地亚 / Cartier)

**Metrics:**
- Search interest index (0-100)
- 7-day change percentage
- China vs Global comparison
- Correlation signals

---

## 🎨 Customization

### Add More Brands

Edit `fetch_trends.py`:

```python
BRANDS = {
    'lv': {'en': 'Louis Vuitton', 'cn': 'LV'},
    'dior': {'en': 'Dior', 'cn': '迪奥'},
    # Add new brand:
    'chanel': {'en': 'Chanel', 'cn': '香奈儿'},
}
```

Then update `dashboard_with_trends.html` to add the color:

```javascript
const BRANDS = {
  // ... existing brands
  chanel: { name: 'Chanel', color: '#000000', keywords: { cn: '香奈儿', en: 'Chanel' } }
};
```

### Change Update Frequency

Edit `.github/workflows/update-trends.yml`:

```yaml
schedule:
  # Every 6 hours:
  - cron: '0 */6 * * *'
  
  # Twice daily (6 AM and 6 PM UTC):
  - cron: '0 6,18 * * *'
```

---

## 🐛 Troubleshooting

### "No data returned"

**Cause:** Google Trends has rate limiting
**Fix:** 
- Wait 10 minutes and run again
- The script has built-in delays (2 seconds between queries)
- GitHub Actions run from different IPs, so less likely to hit limits

### "403 Forbidden" when fetching JSON

**Cause:** Repository is private
**Fix:** Make repo public in Settings → Danger Zone → Change visibility

### Dashboard shows "Loading..." forever

**Cause:** Wrong GitHub URL in dashboard
**Fix:** 
1. Check the fetch URL in dashboard (line ~218)
2. Verify `trends_data.json` exists in your repo
3. Test the URL directly in browser:
   ```
   https://raw.githubusercontent.com/YOUR-USERNAME/luxury-trends-tracker/main/trends_data.json
   ```

### Workflow not running automatically

**Cause:** Workflow permissions
**Fix:**
1. Settings → Actions → General
2. Enable "Read and write permissions"
3. Save

---

## 📊 Reading the Dashboard

### KPI Cards

```
Search Interest: 67 ↑ +12%
```
- **67**: Current search interest index (0-100 scale)
- **↑**: Trending up
- **+12%**: Change vs. 7 days ago

### Signal Analysis

**✓ Strong Buy Signal**
- Both China and Global trending up
- Coordinated demand across markets

**⚠ Mixed Signal**
- China up, Global flat (or vice versa)
- Regional divergence

**✗ Weak Signal**
- Both markets declining
- Broad softness in demand

---

## 💡 Using This for LVMH Analysis

### Leading Indicators

1. **Search spikes BEFORE earnings:**
   - If China search ↑ before quarterly report
   - Might indicate strong sales coming

2. **China vs Global divergence:**
   - China down, Global up → China-specific headwinds
   - China up, Global down → China resilience

3. **Correlation with stock price:**
   - Track search trends vs LVMH stock
   - Look for patterns before earnings beats/misses

### Combining with Other Data

```
Strong Buy Signal:
✓ Google Trends (China) ↑
✓ Google Trends (Global) ↑
✓ WeChat Index ↑
✓ NPS Value stable/improving

Avoid:
✗ Google Trends ↓
✗ WeChat Index ↓
✗ NPS declining
```

---

## 🔐 Data Privacy

- ✅ All data is public (Google Trends aggregated search data)
- ✅ No personal information collected
- ✅ No API keys needed
- ✅ Runs in GitHub's infrastructure (not your computer)

---

## 📈 Next Steps

1. **Backtest correlation:**
   - Download historical trends (12 months)
   - Compare with LVMH quarterly earnings
   - Look for predictive patterns

2. **Add alerts:**
   - Create GitHub Action to email you when trends spike
   - Set thresholds (e.g., +20% in 7 days)

3. **Integrate with trading:**
   - Export trends_data.json to your trading system
   - Automate buy/sell signals based on thresholds

---

## 📝 Files Summary

| File | Purpose | Location |
|------|---------|----------|
| `fetch_trends.py` | Fetches Google Trends data | Root |
| `update-trends.yml` | GitHub Actions automation | `.github/workflows/` |
| `dashboard_with_trends.html` | Visual dashboard | Root |
| `trends_data.json` | Auto-generated data file | Root (created by script) |

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Repository is public
- [ ] All 3 files uploaded correctly
- [ ] GitHub Actions has write permissions
- [ ] Workflow enabled in Actions tab
- [ ] Manual test run completed successfully
- [ ] `trends_data.json` exists in repo
- [ ] Dashboard URL updated with your username
- [ ] Dashboard loads and shows data

---

## 🆘 Need Help?

Common issues and solutions above. If stuck:

1. Check GitHub Actions logs (Actions tab → Click workflow run → View logs)
2. Test `fetch_trends.py` locally first
3. Verify all URLs match your actual GitHub username/repo name

---

**You're all set! 🎉**

The system will now run automatically every day, giving you fresh luxury brand search data from China and globally.
