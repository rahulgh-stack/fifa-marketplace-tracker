#!/usr/bin/env python3
"""
Retry failed matches that have 0 listings
"""

import asyncio
import json
import os
import re
from datetime import datetime
from playwright.async_api import async_playwright

# Failed matches that need retry
FAILED_MATCHES = [17, 41, 56, 67, 77, 91, 24, 53, 79, 92, 28, 48, 66, 36, 54, 75]

async def scrape_single_match(page, match_num):
    """Scrape a single match"""
    tag = f"m{match_num}"
    url = f"https://collect.fifa.com/marketplace?tags={tag}"
    
    listings = []
    
    try:
        print(f"Retrying {tag}...")
        await page.goto(url, wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(4000)  # Longer wait
        
        # Find price elements
        price_elements = await page.query_selector_all('text=/US\\$/')
        
        for j, price_elem in enumerate(price_elements[:15]):
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
                    
                    listing_data = {
                        'tag': tag,
                        'price': price_match.group() if price_match else '',
                        'text': text_content.strip()
                    }
                    
                    # Extract title
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
                    
                    if 'NO LONGER VALID' not in text_content.upper():
                        listings.append(listing_data)
                        
            except Exception as e:
                continue
        
        result = {
            "tag": tag,
            "url": url,
            "listings_count": len(listings),
            "listings": listings,
            "success": True,
            "timestamp": datetime.now().isoformat()
        }
        
        # Save result
        output_dir = "fifa_complete_20250723_115019"
        filepath = os.path.join(output_dir, f"{tag}.json")
        
        with open(filepath, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"✅ {tag}: {len(listings)} listings")
        return result
        
    except Exception as e:
        print(f"❌ {tag}: {str(e)}")
        return None

async def main():
    """Retry all failed matches"""
    print(f"Retrying {len(FAILED_MATCHES)} failed matches...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        successful = 0
        
        for match_num in FAILED_MATCHES:
            result = await scrape_single_match(page, match_num)
            if result and result.get('success') and len(result.get('listings', [])) > 0:
                successful += 1
            
            # Delay between requests
            await asyncio.sleep(2)
        
        await browser.close()
        
        print(f"\n✅ Successfully updated {successful}/{len(FAILED_MATCHES)} matches")

if __name__ == "__main__":
    asyncio.run(main())