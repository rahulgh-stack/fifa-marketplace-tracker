#!/usr/bin/env python3
"""
Retry scraping for the failed matches using the exact working implementation
"""

from playwright.sync_api import sync_playwright
import json
import time
import os
from datetime import datetime

def retry_failed_matches():
    """Retry scraping for the 6 failed matches using working implementation"""
    
    failed_tags = ['m69', 'm70', 'm71', 'm86', 'm87', 'm103']
    output_dir = "fifa_complete_20250723_115019"  # Use the same directory
    
    print(f"Retrying scrape for {len(failed_tags)} failed tags...")
    print(f"Using exact working implementation from complete_remaining.py")
    print(f"Tags to retry: {', '.join(failed_tags)}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})
        
        successful = 0
        failed = 0
        total_listings = 0
        
        for i, tag in enumerate(failed_tags, 1):
            try:
                print(f"[{i}/{len(failed_tags)}] Scraping {tag}...", end=" ")
                
                url = f"https://collect.fifa.com/marketplace?tags={tag}"
                page.goto(url, wait_until='networkidle', timeout=30000)
                page.wait_for_timeout(3000)
                
                # Find price elements - EXACT implementation from complete_remaining.py
                price_elements = page.query_selector_all('text=/US\\$/')
                listings = []
                
                # Extract listings efficiently - EXACT implementation
                for price_elem in price_elements[:15]:
                    try:
                        container = price_elem.evaluate_handle("""
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
                            text_content = container.evaluate("el => el.innerText")
                            
                            # Quick extraction - EXACT implementation
                            import re
                            price_match = re.search(r'US\$[\d,]+\.?\d*', text_content)
                            
                            listing_data = {
                                'tag': tag,
                                'price': price_match.group() if price_match else '',
                                'text': text_content.strip()
                            }
                            
                            # Extract title (first meaningful line) - EXACT implementation
                            lines = [l.strip() for l in text_content.split('\n') if l.strip()]
                            for line in lines:
                                if line and 'US$' not in line and 'From' not in line and len(line) > 10:
                                    listing_data['title'] = line
                                    break
                            else:
                                listing_data['title'] = ''
                            
                            # Extract type - EXACT implementation
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
                
                result = {
                    'tag': tag,
                    'url': url,
                    'listings_count': len(listings),
                    'listings': listings,
                    'success': True,
                    'timestamp': datetime.now().isoformat()
                }
                
                # Save individual result - EXACT implementation
                with open(os.path.join(output_dir, f"{tag}.json"), 'w') as f:
                    json.dump(result, f, indent=2)
                
                successful += 1
                total_listings += len(listings)
                
                print(f"✓ {len(listings)} listings")
                
                # Brief pause - EXACT implementation
                time.sleep(1)
                
            except Exception as e:
                print(f"✗ Error: {str(e)[:50]}")
                result = {
                    'tag': tag,
                    'url': f"https://collect.fifa.com/marketplace?tags={tag}",
                    'error': str(e),
                    'success': False,
                    'timestamp': datetime.now().isoformat()
                }
                
                # Save error result
                with open(os.path.join(output_dir, f"{tag}.json"), 'w') as f:
                    json.dump(result, f, indent=2)
                
                failed += 1
        
        browser.close()
        
        print(f"\n🏁 RETRY COMPLETE:")
        print(f"   ✅ Successful: {successful}")
        print(f"   ❌ Failed: {failed}")
        print(f"   📊 Total listings: {total_listings}")
        print(f"   📁 Files updated in: {output_dir}/")

if __name__ == "__main__":
    retry_failed_matches()
