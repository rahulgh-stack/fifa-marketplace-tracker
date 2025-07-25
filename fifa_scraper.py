#!/usr/bin/env python3
"""
FIFA World Cup 2026 Marketplace Scraper
- Constant folder name: fifa_marketplace_data
- Only update JSON if scraping succeeds
- Preserve old data if scraping fails
"""

import asyncio
import json
import os
import re
from datetime import datetime
from playwright.async_api import async_playwright

# Constant data directory name
DATA_DIR = "fifa_marketplace_data"

async def scrape_match(page, match_num):
    """Scrape a single match with error handling"""
    tag = f"m{match_num}"
    url = f"https://collect.fifa.com/marketplace?tags={tag}"
    
    try:
        print(f"Scraping {tag}...")
        await page.goto(url, wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(3000)
        
        # Find price elements
        price_elements = await page.query_selector_all('text=/US\\$/')
        listings = []
        
        for price_elem in price_elements[:15]:
            try:
                container = await price_elem.evaluate_handle("""
                    (el) => {
                        let parent = el;
                        for (let i = 0; i < 8; i++) {
                            parent = parent.parentElement;
                            if (!parent) break;
                            if (parent.querySelector('img') || parent.querySelector('h3')) {
                                return parent;
                            }
                        }
                        return parent;
                    }
                """)
                
                if container:
                    text_content = await container.evaluate("el => el.innerText")
                    price_match = re.search(r'US\$[\d,]+\.?\d*', text_content)
                    
                    if price_match and 'NO LONGER VALID' not in text_content.upper():
                        listing_data = {
                            'tag': tag,
                            'price': price_match.group(),
                            'text': text_content.strip()
                        }
                        
                        # Extract title (first meaningful line)
                        lines = [l.strip() for l in text_content.split('\\n') if l.strip()]
                        for line in lines:
                            if line and 'US$' not in line and 'From' not in line and len(line) > 10:
                                listing_data['title'] = line
                                break
                        
                        # Extract type
                        if 'Iconic' in text_content:
                            listing_data['type'] = 'Iconic'
                        elif 'Rare' in text_content:
                            listing_data['type'] = 'Rare'
                        elif 'Epic' in text_content:
                            listing_data['type'] = 'Epic'
                        else:
                            listing_data['type'] = ''
                        
                        listings.append(listing_data)
                        
            except Exception:
                continue
        
        if len(listings) > 0:  # Only return success if we got listings
            return {
                "tag": tag,
                "url": url,
                "listings_count": len(listings),
                "listings": listings,
                "success": True,
                "timestamp": datetime.now().isoformat()
            }
        else:
            return None  # Failed - no listings found
            
    except Exception as e:
        print(f"Error scraping {tag}: {e}")
        return None  # Failed

def save_match_data(match_data, match_num):
    """Save match data only if scraping succeeded"""
    if match_data is None:
        print(f"⚠️  Skipping m{match_num} - scraping failed, keeping old data")
        return False
    
    filepath = os.path.join(DATA_DIR, f"m{match_num}.json")
    
    try:
        with open(filepath, 'w') as f:
            json.dump(match_data, f, indent=2)
        print(f"✅ Updated m{match_num} with {match_data['listings_count']} listings")
        return True
    except Exception as e:
        print(f"❌ Failed to save m{match_num}: {e}")
        return False

async def scrape_matches(match_numbers):
    """Scrape specified matches"""
    # Create data directory if it doesn't exist
    os.makedirs(DATA_DIR, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        successful = 0
        failed = 0
        
        for match_num in match_numbers:
            match_data = await scrape_match(page, match_num)
            
            if save_match_data(match_data, match_num):
                successful += 1
            else:
                failed += 1
            
            # Delay between requests
            await asyncio.sleep(2)
        
        await browser.close()
        
        print(f"\n📊 SUMMARY:")
        print(f"✅ Successfully updated: {successful}")
        print(f"⚠️  Failed/skipped: {failed}")
        
        return successful, failed

async def scrape_all_matches():
    """Scrape all matches 1-104"""
    match_numbers = list(range(1, 105))
    return await scrape_matches(match_numbers)

async def scrape_selected_matches(match_numbers):
    """Scrape only specified matches"""
    return await scrape_matches(match_numbers)

if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 1:
        # Scrape specific matches: python fifa_scraper.py 1 104 7 17
        match_numbers = [int(x) for x in sys.argv[1:]]
        asyncio.run(scrape_selected_matches(match_numbers))
    else:
        # Scrape all matches
        asyncio.run(scrape_all_matches())