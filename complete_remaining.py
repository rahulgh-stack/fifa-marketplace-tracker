from playwright.sync_api import sync_playwright
import json
import time
import os
from datetime import datetime

def complete_scraping():
    """Complete scraping from m30 to m104 in the same format as fifa_complete_20250723_115019"""
    
    # Generate remaining tags (m30 to m104)
    remaining_tags = [f"m{i}" for i in range(30, 105)]
    output_dir = "fifa_complete_20250723_115019"  # Use the same directory
    
    print(f"Completing scrape for remaining {len(remaining_tags)} tags...")
    print(f"Adding to directory: {output_dir}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})
        
        successful = 0
        failed = 0
        total_listings = 0
        
        for i, tag in enumerate(remaining_tags, 30):
            try:
                print(f"[{i}/104] Scraping {tag}...", end=" ")
                
                url = f"https://collect.fifa.com/marketplace?tags={tag}"
                page.goto(url, wait_until='networkidle', timeout=30000)
                page.wait_for_timeout(3000)
                
                # Find price elements
                price_elements = page.query_selector_all('text=/US\\$/')
                listings = []
                
                # Extract listings efficiently
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
                            else:
                                listing_data['title'] = ''
                            
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
                
                failed += 1
            
            # Progress update every 20 tags
            if i % 20 == 0:
                print(f"\n--- Progress: {i}/104 completed, {successful} successful, {total_listings} total listings ---\n")
        
        browser.close()
    
    # Create final summary
    summary = {
        'total_tags_completed': 104,
        'original_tags': '1-29',
        'completed_tags': '30-104', 
        'successful_remaining': successful,
        'failed_remaining': failed,
        'total_listings_added': total_listings,
        'completion_timestamp': datetime.now().isoformat(),
        'output_directory': output_dir
    }
    
    with open(os.path.join(output_dir, "completion_summary.json"), 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n=== COMPLETION RESULTS ===")
    print(f"Remaining tags scraped: {len(remaining_tags)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total listings added: {total_listings}")
    print(f"Directory: {output_dir}")
    
    return summary

if __name__ == "__main__":
    complete_scraping()