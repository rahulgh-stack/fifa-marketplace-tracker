# 🏆 FIFA World Cup 2026 Marketplace Tracker

A comprehensive web scraper and data visualization tool for tracking FIFA Collect marketplace prices for FIFA World Cup 2026 "Right to Buy" (RTB) collectibles.

## 🌐 Live Website

**View the live marketplace data**: [https://rahulgh-stack.github.io/fifa-marketplace-tracker/](https://rahulgh-stack.github.io/fifa-marketplace-tracker/)

## 📊 Features

- **Complete Tournament Coverage**: All 104 FIFA World Cup 2026 matches tracked
- **Real-time Marketplace Data**: Prices ranging from $179 to $52,700
- **Mobile Responsive Design**: Optimized for all devices
- **Interactive Sorting**: Sortable table by date, price, venue, country, etc.
- **Data Quality Filtering**: Excludes "NO LONGER VALID" listings for accurate pricing
- **Comprehensive Match Info**: Venue, country, stadium, stage, and date details

## 🗃️ Dataset

The `fifa_marketplace_data/` directory contains:
- **104 venue JSON files** (m1.json - m104.json) with marketplace data
- **1,152+ valid marketplace listings** collected from FIFA Collect
- **Complete tournament schedule** with venue and stadium information

## 🚀 Quick Start

1. **View the Website**: Visit the [live GitHub Pages site](https://rahulgh-stack.github.io/fifa-marketplace-tracker/)

2. **Generate Updated Data**:
   ```bash
   python3 create_website.py
   ```

3. **Run Full Scraper** (if needed):
   ```bash
   python3 fifa_scraper.py
   ```

## 🛠️ Technical Stack

- **Web Scraping**: Playwright for browser automation
- **Data Processing**: Python with JSON handling
- **Frontend**: Pure HTML/CSS/JavaScript (mobile-responsive)
- **Deployment**: GitHub Pages

## 📁 Project Structure

```
├── index.html                          # GitHub Pages main file
├── create_website.py                   # Website generator
├── fifa_scraper.py                     # Complete marketplace scraper
├── fifa_marketplace_data/              # Complete dataset
│   └── m1.json - m104.json            # Individual venue data (104 files)
├── requirements.txt                    # Python dependencies
└── CLEAN_PROJECT_STRUCTURE.md          # Project documentation
```

## 🌍 FIFA World Cup 2026

The tournament will be held across **USA, Canada, and Mexico** from **June 11 - July 19, 2026**, featuring:
- **48 teams** (expanded format)
- **104 matches** total
- **16 host cities** across North America
- **FIFA Collect RTB** collectibles for priority ticket access

## 📈 Data Insights

- **Price Range**: $179 - $52,700 for RTB collectibles
- **Valid Listings**: 1,152+ active marketplace entries
- **Most Expensive**: Final match collectibles reach $52,700
- **Most Affordable**: Group stage matches start at $179
- **Coverage**: 100% of FIFA World Cup 2026 venues tracked

## 🔄 Updates

The website automatically filters out expired "NO LONGER VALID" listings and displays real-time marketplace data. Run `python3 create_website.py` to generate the latest version with current data.

---

**Built with ❤️ for FIFA World Cup 2026 • Last updated: July 25, 2025**

## 📊 Dataset: `fifa_marketplace_data/`

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

### Scrape All Tags (m1-m104)
```bash
python3 fifa_scraper.py
```

## 📦 Installation

```bash
# Install dependencies
pip3 install playwright

# Install browser
playwright install chromium
```


## 📈 Dataset Statistics

- **Total Venues**: 104 ✅
- **Total Listings**: 1,152+ 
- **Success Rate**: 100% (all venues scraped)
- **Collection Date**: July 25, 2025
- **Price Range**: US$269 - US$52,700+

## 🏆 About FIFA Collect

FIFA Collect marketplace sells official collectible NFTs that function as "Right to Buy" (RTB) tickets for FIFA World Cup 26™ matches. Each collectible grants the holder priority access to purchase actual match tickets for specific venues.

**Venue Coverage**: All 104 FIFA World Cup 26™ venues across USA, Canada, and Mexico.