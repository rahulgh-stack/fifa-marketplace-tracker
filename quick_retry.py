#!/usr/bin/env python3
import asyncio
import json
import os
import re
from datetime import datetime
from playwright.async_api import async_playwright

# Still failed matches
REMAINING = [77, 91, 24, 53, 79, 92, 28, 48, 66, 36, 54, 75]

async def scrape_one(match_num):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        tag = f"m{match_num}"
        url = f"https://collect.fifa.com/marketplace?tags={tag}"
        
        try:
            await page.goto(url, wait_until='networkidle', timeout=30000)
            await page.wait_for_timeout(5000)
            
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
                                'text': text_content.strip(),
                                'type': 'Iconic' if 'Iconic' in text_content else 'Rare' if 'Rare' in text_content else 'Epic' if 'Epic' in text_content else ''
                            }
                            
                            lines = [l.strip() for l in text_content.split('\\n') if l.strip()]
                            for line in lines:
                                if line and 'US$' not in line and 'From' not in line and len(line) > 10:
                                    listing_data['title'] = line
                                    break
                            
                            listings.append(listing_data)
                except:
                    continue
            
            result = {
                "tag": tag,
                "url": url,
                "listings_count": len(listings),
                "listings": listings,
                "success": True,
                "timestamp": datetime.now().isoformat()
            }
            
            with open(f"fifa_complete_20250723_115019/{tag}.json", 'w') as f:
                json.dump(result, f, indent=2)
            
            print(f"{tag}: {len(listings)} listings")
            
        except Exception as e:
            print(f"{tag}: ERROR - {e}")
        finally:
            await browser.close()

async def main():
    for match_num in REMAINING:
        await scrape_one(match_num)
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())