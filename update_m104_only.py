#!/usr/bin/env python3
"""
Update just m104 (Final) specifically
"""

import asyncio
import json
import os
import re
from datetime import datetime
from playwright.async_api import async_playwright

async def scrape_m104():
    """Scrape data for m104 (Final)"""
    tag = "m104"
    url = f"https://collect.fifa.com/marketplace?tags={tag}"
    
    listings = []
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            print(f"Scraping {tag}...")
            await page.goto(url, wait_until='networkidle', timeout=30000)
            
            # Wait for listings to load
            await page.wait_for_timeout(3000)
            
            # Find price elements using the same approach as original scraper
            price_elements = await page.query_selector_all('text=/US\\$/')
            
            for j, price_elem in enumerate(price_elements[:15]):  # Limit to 15 items
                try:
                    # Get the container element by traversing up the DOM
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
                        
                        # Extract price using regex
                        price_match = re.search(r'US\$[\d,]+\.?\d*', text_content)
                        
                        listing_data = {
                            'tag': tag,
                            'price': price_match.group() if price_match else '',
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
                        
                        # Skip if NO LONGER VALID
                        if 'NO LONGER VALID' not in text_content.upper():
                            listings.append(listing_data)
                        
                except Exception as e:
                    continue
            
            await browser.close()
        
        print(f"Found {len(listings)} valid listings for {tag}")
        
        result = {
            "tag": tag,
            "url": url,
            "listings_count": len(listings),
            "listings": listings,
            "success": True,
            "timestamp": datetime.now().isoformat()
        }
        
        # Save individual match file
        output_dir = "fifa_complete_20250723_115019"
        filename = f"m104.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"Saved {filename}")
        return result
        
    except Exception as e:
        print(f"Error scraping {tag}: {e}")
        return {
            "tag": tag,
            "url": url,
            "error": str(e),
            "success": False,
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    asyncio.run(scrape_m104())