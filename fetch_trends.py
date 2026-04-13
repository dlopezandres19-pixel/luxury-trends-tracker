#!/usr/bin/env python3
"""
Google Trends Data Fetcher for Luxury Brands
Tracks: Louis Vuitton, Dior, Hermès, Gucci, Cartier
Regions: China (primary focus) + Global (comparison)
Updated: Now includes 7 days, 30 days, and 12 months
"""

from pytrends.request import TrendReq
import pandas as pd
from datetime import datetime
import json
import time
import os

# Configuration
BRANDS = {
    'lv': {'en': 'Louis Vuitton', 'cn': 'LV'},
    'dior': {'en': 'Dior', 'cn': '迪奥'},
    'hermes': {'en': 'Hermès', 'cn': '爱马仕'},
    'gucci': {'en': 'Gucci', 'cn': 'Gucci'},
    'cartier': {'en': 'Cartier', 'cn': '卡地亚'}
}

def fetch_trends_data(keywords, timeframe, geo='', label=''):
    print(f"Fetching {label}...")
    
    for attempt in range(3):
        try:
            pytrends = TrendReq(
                hl='zh-CN',
                tz=360,
                timeout=(10, 25),
                retries=3,
                backoff_factor=0.5,
                requests_args={
                    'headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Accept-Encoding': 'gzip, deflate, br',
                    }
                }
            )
            pytrends.build_payload(keywords, timeframe=timeframe, geo=geo)
            
            df = pytrends.interest_over_time()
            
            if df.empty:
                print(f"  ⚠ No data returned for {label} (attempt {attempt+1}/3)")
                time.sleep(10)
                continue
            
            # Remove 'isPartial' column if present
            if 'isPartial' in df.columns:
                df = df.drop('isPartial', axis=1)
            
            # Convert to format suitable for dashboard
            data = {
                'labels': [d.strftime('%Y-%m-%d') for d in df.index],
                'datasets': {}
            }
            
            for col in df.columns:
                data['datasets'][col] = df[col].tolist()
            
            # Calculate averages
            data['averages'] = {col: float(df[col].mean()) for col in df.columns}
            
            # Calculate latest values and changes
            data['latest'] = {}
            for col in df.columns:
                latest_val = float(df[col].iloc[-1])
                lookback = min(7, len(df) - 1) if 'now 7-d' in timeframe else min(30, len(df) - 1) if 'today 1-m' in timeframe else len(df) - 1
                prev_val = float(df[col].iloc[-lookback-1] if len(df) > lookback else df[col].iloc[0])
                change = ((latest_val - prev_val) / prev_val * 100) if prev_val > 0 else 0
                
                data['latest'][col] = {
                    'value': latest_val,
                    'change': round(change, 1)
                }
            
            print(f"  ✓ Retrieved {len(df)} data points")
            return data
            
        except Exception as e:
            print(f"  ✗ Error (attempt {attempt+1}/3): {e}")
            time.sleep(10)
    
    print(f"  ✗ All attempts failed for {label}")
    return None

def main():
    print("=" * 70)
    print("GOOGLE TRENDS - LUXURY BRANDS TRACKER")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    output = {
        'metadata': {
            'last_update': datetime.now().isoformat(),
            'brands': list(BRANDS.keys()),
            'regions': ['china', 'global']
        },
        'china': {},
        'global': {}
    }
    
    keywords_cn = [BRANDS[b]['cn'] for b in BRANDS.keys()]
    keywords_en = [BRANDS[b]['en'] for b in BRANDS.keys()]

    # CHINA - Last 7 days
    print("\n[1/6] China - Last 7 days")
    print("-" * 70)
    data = fetch_trends_data(keywords_cn, 'now 7-d', 'CN', 'China 7d')
    if data:
        output['china']['7d'] = data
    time.sleep(8)

    # CHINA - Last 30 days
    print("\n[2/6] China - Last 30 days")
    print("-" * 70)
    data = fetch_trends_data(keywords_cn, 'today 1-m', 'CN', 'China 30d')
    if data:
        output['china']['30d'] = data
    time.sleep(8)

    # CHINA - Last 12 months
    print("\n[3/6] China - Last 12 months")
    print("-" * 70)
    data = fetch_trends_data(keywords_cn, 'today 12-m', 'CN', 'China 12m')
    if data:
        output['china']['12m'] = data
    time.sleep(8)

    # GLOBAL - Last 7 days
    print("\n[4/6] Global - Last 7 days")
    print("-" * 70)
    data = fetch_trends_data(keywords_en, 'now 7-d', '', 'Global 7d')
    if data:
        output['global']['7d'] = data
    time.sleep(8)

    # GLOBAL - Last 30 days
    print("\n[5/6] Global - Last 30 days")
    print("-" * 70)
    data = fetch_trends_data(keywords_en, 'today 1-m', '', 'Global 30d')
    if data:
        output['global']['30d'] = data
    time.sleep(8)

    # GLOBAL - Last 12 months
    print("\n[6/6] Global - Last 12 months")
    print("-" * 70)
    data = fetch_trends_data(keywords_en, 'today 12-m', '', 'Global 12m')
    if data:
        output['global']['12m'] = data

    # Save to JSON file
    output_file = 'trends_data.json'
    print(f"\n{'=' * 70}")
    print(f"Saving data to {output_file}...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Data saved successfully")
    print(f"  File size: {os.path.getsize(output_file)} bytes")
    print(f"{'=' * 70}\n")

    # Print summary
    print("SUMMARY:")
    if 'china' in output and '7d' in output['china']:
        print("\nChina (Last 7 days):")
        for brand, data in output['china']['7d']['latest'].items():
            change_symbol = '↑' if data['change'] > 0 else '↓' if data['change'] < 0 else '→'
            print(f"  {brand:15s}: {data['value']:5.1f} {change_symbol} {abs(data['change']):5.1f}%")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
