#!/usr/bin/env python3
"""
Update selected FIFA World Cup 2026 marketplace data:
- m104 (Final)
- NYC area games (East Rutherford)
- Mexico games (Mexico City, Zapopan, Guadalupe)
"""

import asyncio
import json
import os
import random
from datetime import datetime
from playwright.async_api import async_playwright

async def scrape_tag(page, tag_number):
    """Scrape data for a specific match tag"""
    tag = f"m{tag_number}"
    url = f"https://collect.fifa.com/marketplace?tags={tag}"
    
    listings = []
    
    try:
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
                    import re
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
        
        print(f"Found {len(listings)} valid listings for {tag}")
        
        return {
            "tag": tag,
            "url": url,
            "listings_count": len(listings),
            "listings": listings,
            "success": True,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Error scraping {tag}: {e}")
        return {
            "tag": tag,
            "url": url,
            "error": str(e),
            "success": False,
            "timestamp": datetime.now().isoformat()
        }

async def main():
    """Main scraping function for selected matches"""
    
    # Define matches to update
    selected_matches = [
        # Final
        104,
        
        # NYC area games (East Rutherford)
        7, 17, 41, 56, 67, 77, 91,
        
        # Mexico games
        1, 24, 53, 79, 92,  # Mexico City
        2, 28, 48, 66,      # Zapopan
        12, 36, 54, 75      # Guadalupe
    ]
    
    # Remove duplicates and sort
    selected_matches = sorted(list(set(selected_matches)))
    
    print(f"Will update {len(selected_matches)} matches: {selected_matches}")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        results = []
        
        for match_num in selected_matches:
            result = await scrape_tag(page, match_num)
            results.append(result)
            
            # Save individual match file
            output_dir = "fifa_complete_20250723_115019"
            filename = f"m{match_num}.json"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w') as f:
                json.dump(result, f, indent=2)
            
            print(f"Saved {filename}")
            
            # Random delay between requests
            delay = random.uniform(1, 3)
            await asyncio.sleep(delay)
        
        await browser.close()
    
    # Create summary
    summary = {
        "update_timestamp": datetime.now().isoformat(),
        "matches_updated": len(selected_matches),
        "match_numbers": selected_matches,
        "successful": sum(1 for r in results if r['success']),
        "failed": sum(1 for r in results if not r['success'])
    }
    
    with open('update_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\nUpdate Summary:")
    print(f"Total matches updated: {summary['matches_updated']}")
    print(f"Successful: {summary['successful']}")
    print(f"Failed: {summary['failed']}")

if __name__ == "__main__":
    asyncio.run(main())