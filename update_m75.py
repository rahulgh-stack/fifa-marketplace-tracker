#!/usr/bin/env python3
import asyncio
import json
import re
from datetime import datetime
from playwright.async_api import async_playwright

async def scrape_m75():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        url = "https://collect.fifa.com/marketplace?tags=m75"
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
                        listings.append({
                            'tag': 'm75',
                            'price': price_match.group(),
                            'text': text_content.strip(),
                            'type': 'Iconic' if 'Iconic' in text_content else 'Rare' if 'Rare' in text_content else 'Epic' if 'Epic' in text_content else ''
                        })
            except:
                continue
        
        result = {
            "tag": "m75",
            "url": url,
            "listings_count": len(listings),
            "listings": listings,
            "success": True,
            "timestamp": datetime.now().isoformat()
        }
        
        with open("fifa_complete_20250723_115019/m75.json", 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"m75: {len(listings)} listings")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_m75())