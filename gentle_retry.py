#!/usr/bin/env python3
"""
Gently retry the remaining failed matches one by one with proper delays
"""

import asyncio
import json
import os
import re
from datetime import datetime
from playwright.async_api import async_playwright

# Remaining failed matches
REMAINING = [79, 48, 66, 36, 54, 75]

async def gentle_scrape_one(match_num):
    """Gently scrape one match with proper delays"""
    tag = f"m{match_num}"
    url = f"https://collect.fifa.com/marketplace?tags={tag}"
    
    print(f"\n🔄 Gently scraping {tag}...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})
        
        try:
            # Navigate with patience
            print(f"   📡 Loading {url}...")
            await page.goto(url, wait_until='networkidle', timeout=45000)
            
            # Wait generously for content to load
            print(f"   ⏳ Waiting 6 seconds for content...")
            await page.wait_for_timeout(6000)
            
            # Find price elements
            print(f"   🔍 Looking for price elements...")
            price_elements = await page.query_selector_all('text=/US\\$/')
            print(f"   💰 Found {len(price_elements)} price elements")
            
            listings = []
            
            for i, price_elem in enumerate(price_elements[:15]):
                try:
                    print(f"   📋 Processing listing {i+1}...")
                    
                    # Get container with patience
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
                                'text': text_content.strip(),
                                'type': 'Iconic' if 'Iconic' in text_content else 'Rare' if 'Rare' in text_content else 'Epic' if 'Epic' in text_content else ''
                            }
                            
                            # Extract title
                            lines = [l.strip() for l in text_content.split('\\n') if l.strip()]
                            for line in lines:
                                if line and 'US$' not in line and 'From' not in line and len(line) > 10:
                                    listing_data['title'] = line
                                    break
                            
                            listings.append(listing_data)
                            print(f"   ✅ Added listing: {price_match.group()}")
                        
                except Exception as e:
                    print(f"   ⚠️  Skipped listing {i+1}: {str(e)[:50]}")
                    continue
            
            # Create result
            result = {
                "tag": tag,
                "url": url,
                "listings_count": len(listings),
                "listings": listings,
                "success": True,
                "timestamp": datetime.now().isoformat()
            }
            
            # Save result
            filepath = f"fifa_complete_20250723_115019/{tag}.json"
            with open(filepath, 'w') as f:
                json.dump(result, f, indent=2)
            
            print(f"   🎉 SUCCESS: {tag} saved with {len(listings)} listings")
            return len(listings)
            
        except Exception as e:
            print(f"   ❌ ERROR scraping {tag}: {str(e)}")
            return 0
            
        finally:
            await browser.close()

async def main():
    """Gently process all remaining matches"""
    print("🌟 Starting gentle retry of remaining matches...")
    print(f"📋 Matches to process: {REMAINING}")
    
    total_success = 0
    
    for i, match_num in enumerate(REMAINING, 1):
        print(f"\n{'='*50}")
        print(f"🎯 Processing match {i}/{len(REMAINING)}: m{match_num}")
        print(f"{'='*50}")
        
        listings_count = await gentle_scrape_one(match_num)
        if listings_count > 0:
            total_success += 1
        
        # Gentle delay between matches
        if i < len(REMAINING):
            print(f"   😴 Resting 3 seconds before next match...")
            await asyncio.sleep(3)
    
    print(f"\n🏆 FINAL RESULTS:")
    print(f"✅ Successfully updated: {total_success}/{len(REMAINING)} matches")
    print(f"❌ Still failed: {len(REMAINING) - total_success} matches")

if __name__ == "__main__":
    asyncio.run(main())