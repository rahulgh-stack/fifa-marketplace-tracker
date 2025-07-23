# FIFA Collect Marketplace Scraper

Complete dataset of FIFA Collect marketplace listings for all venue tags (m1 to m104).

## 📊 Dataset: `fifa_complete_20250723_115019/`

**Status: ✅ COMPLETE** - All 104 venue tags successfully scraped with 1,152+ total listings.

### Sample Data Structure
```json
{
  "tag": "m104",
  "url": "https://collect.fifa.com/marketplace?tags=m104",
  "listings_count": 15,
  "listings": [
    {
      "tag": "m104",
      "price": "US$6,999.00",
      "text": "COLLECTIBLE ALSO VALID AS RTB FOR 1 TICKET TO M104 NEW YORK\nIconic\nFROM OPENING TO FINAL PASSING BY HOUSTON\nFrom\nUS$6,999.00",
      "title": "COLLECTIBLE ALSO VALID AS RTB FOR 1 TICKET TO M104 NEW YORK",
      "type": "Iconic"
    }
  ],
  "success": true,
  "timestamp": "2025-07-23T12:45:40.682984"
}
```

### 💰 Price Ranges Found
- **m1 (Mexico City)**: US$3,147 - US$52,700
- **m69 (Kansas City)**: US$269 - US$709
- **m83 (Toronto)**: US$284 - US$700
- **m103 (Miami)**: US$315 - US$339
- **m104 (New York Finals)**: US$6,999 - US$16,500

### 🎯 Item Types
- **Iconic** - Most common tier
- **Epic** - Mid-tier collectibles  
- **Rare** - Premium collectibles
- **RTB** - Right to Buy tickets for FIFA World Cup 26™ events

## 🚀 Usage

### Re-scrape All Tags (m1-m104)
```bash
python3 final_scraper.py
```

### Re-scrape Specific Range
```bash
python3 complete_remaining.py
```

### Retry Failed Tags Only
```bash
python3 retry_failed_exact.py
```

## 📦 Installation

```bash
# Install dependencies
pip3 install playwright

# Install browser
playwright install chromium
```

## 📁 Project Structure

```
fifa_complete_20250723_115019/    # Complete dataset (105 files)
├── completion_summary.json       # Scraping summary
├── m1.json                      # Mexico City venue
├── m2.json                      # Next venue
├── ...                          # All venues m1-m104
└── m104.json                    # New York Finals

Scripts:
├── final_scraper.py             # Complete scraper (m1-m104)
├── complete_remaining.py        # Range scraper (m30-m104) 
└── retry_failed_exact.py        # Retry failed tags
```

## 📈 Dataset Statistics

- **Total Venues**: 104 ✅
- **Total Listings**: 1,152+ 
- **Success Rate**: 100% (all venues scraped)
- **Collection Date**: July 23, 2025
- **Price Range**: US$269 - US$52,700+

## 🏆 About FIFA Collect

FIFA Collect marketplace sells official collectible NFTs that function as "Right to Buy" (RTB) tickets for FIFA World Cup 26™ matches. Each collectible grants the holder priority access to purchase actual match tickets for specific venues.

**Venue Coverage**: All 104 FIFA World Cup 26™ venues across USA, Canada, and Mexico.