from playwright.sync_api import sync_playwright
import json
import time
import os
from datetime import datetime
from typing import List, Dict, Any

def scrape_fifa_complete():
    """Scrape all FIFA marketplace tags from m1 to m104 efficiently"""
    
    # Generate all tags
    tags = [f"m{i}" for i in range(1, 105)]
    output_dir = f"fifa_complete_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Starting comprehensive scrape of {len(tags)} tags...")
    print(f"Output directory: {output_dir}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})
        
        results = []
        successful = 0
        failed = 0
        total_listings = 0
        
        for i, tag in enumerate(tags, 1):
            try:
                print(f"[{i}/{len(tags)}] Scraping {tag}...", end=" ")
                
                url = f"https://collect.fifa.com/marketplace?tags={tag}"
                page.goto(url, wait_until='networkidle', timeout=30000)
                page.wait_for_timeout(3000)  # Reduced wait time
                
                # Find price elements
                price_elements = page.query_selector_all('text=/US\\$/')
                listings = []
                
                # Extract listings efficiently
                for j, price_elem in enumerate(price_elements[:15]):  # Limit per page
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
                            
                            # Quick extraction
                            import re
                            price_match = re.search(r'US\$[\d,]+\.?\d*', text_content)
                            
                            listing_data = {
                                'tag': tag,
                                'price': price_match.group() if price_match else '',
                                'text': text_content.strip()
                            }
                            
                            # Extract title (first meaningful line)
                            lines = [l.strip() for l in text_content.split('\n') if l.strip()]
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
                            
                            listings.append(listing_data)
                            
                    except Exception as e:
                        continue
                
                result = {
                    'tag': tag,
                    'url': url,
                    'listings_count': len(listings),
                    'listings': listings,
                    'success': True,
                    'timestamp': datetime.now().isoformat()
                }
                
                # Save individual result
                with open(os.path.join(output_dir, f"{tag}.json"), 'w') as f:
                    json.dump(result, f, indent=2)
                
                results.append(result)
                successful += 1
                total_listings += len(listings)
                
                print(f"✓ {len(listings)} listings")
                
                # Brief pause
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
                
                with open(os.path.join(output_dir, f"{tag}.json"), 'w') as f:
                    json.dump(result, f, indent=2)
                
                results.append(result)
                failed += 1
            
            # Progress update every 20 tags
            if i % 20 == 0:
                print(f"\n--- Progress: {i}/{len(tags)} completed, {successful} successful, {total_listings} total listings ---\n")
        
        browser.close()
    
    # Save combined results
    with open(os.path.join(output_dir, "all_results.json"), 'w') as f:
        json.dump(results, f, indent=2)
    
    # Save summary
    summary = {
        'total_tags': len(tags),
        'successful': successful,
        'failed': failed,
        'total_listings': total_listings,
        'timestamp': datetime.now().isoformat(),
        'output_directory': output_dir
    }
    
    with open(os.path.join(output_dir, "summary.json"), 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n=== FINAL RESULTS ===")
    print(f"Total tags scraped: {len(tags)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total listings found: {total_listings}")
    print(f"Output directory: {output_dir}")
    
    return summary

if __name__ == "__main__":
    scrape_fifa_complete()