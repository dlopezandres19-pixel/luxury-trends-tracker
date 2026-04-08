#!/usr/bin/env python3
"""
Google Trends Data Fetcher for Luxury Brands
Tracks: Louis Vuitton, Dior, Hermès, Gucci, Cartier
Regions: China (primary focus) + Global (comparison)
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
    """
    Fetch Google Trends data for given keywords
    
    Args:
        keywords: List of search terms
        timeframe: Time period (e.g., 'now 7-d', 'today 12-m')
        geo: Geographic region code (e.g., 'CN' for China, '' for global)
        label: Label for this dataset
    
    Returns:
        Dictionary with processed data
    """
    print(f"Fetching {label}...")
    
    try:
        pytrends = TrendReq(hl='zh-CN', tz=360, timeout=(10, 25))
        pytrends.build_payload(keywords, timeframe=timeframe, geo=geo)
        
        df = pytrends.interest_over_time()
        
        if df.empty:
            print(f"  ⚠ No data returned for {label}")
            return None
        
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
            prev_val = float(df[col].iloc[-8] if len(df) > 7 else df[col].iloc[0])  # Compare to 7 days ago
            change = ((latest_val - prev_val) / prev_val * 100) if prev_val > 0 else 0
            
            data['latest'][col] = {
                'value': latest_val,
                'change': round(change, 1)
            }
        
        print(f"  ✓ Retrieved {len(df)} data points")
        return data
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return None

def main():
    """Main execution function"""
    
    print("=" * 70)
    print("GOOGLE TRENDS - LUXURY BRANDS TRACKER")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    # Prepare output structure
    output = {
        'metadata': {
            'last_update': datetime.now().isoformat(),
            'brands': list(BRANDS.keys()),
            'regions': ['china', 'global']
        },
        'china': {},
        'global': {}
    }
    
    # Get Chinese keywords
    keywords_cn = [BRANDS[b]['cn'] for b in BRANDS.keys()]
    keywords_en = [BRANDS[b]['en'] for b in BRANDS.keys()]
    
    # CHINA - Last 7 days
    print("\n[1/4] China - Last 7 days")
    print("-" * 70)
    data = fetch_trends_data(keywords_cn, 'now 7-d', 'CN', 'China 7d')
    if data:
        output['china']['7d'] = data
        time.sleep(2)  # Rate limiting
    
    # CHINA - Last 12 months
    print("\n[2/4] China - Last 12 months")
    print("-" * 70)
    data = fetch_trends_data(keywords_cn, 'today 12-m', 'CN', 'China 12m')
    if data:
        output['china']['12m'] = data
        time.sleep(2)
    
    # GLOBAL - Last 7 days
    print("\n[3/4] Global - Last 7 days")
    print("-" * 70)
    data = fetch_trends_data(keywords_en, 'now 7-d', '', 'Global 7d')
    if data:
        output['global']['7d'] = data
        time.sleep(2)
    
    # GLOBAL - Last 12 months
    print("\n[4/4] Global - Last 12 months")
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
