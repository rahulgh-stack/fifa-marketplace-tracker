#!/usr/bin/env python3
"""
Create FIFA World Cup 2026 Marketplace Data Website
"""

import json
import os
import re
from datetime import datetime

def parse_price(price_str):
    """Extract numeric value from price string like 'US$6,999.00'"""
    if not price_str:
        return 0
    # Remove currency symbols, commas, and convert to float
    numeric = re.sub(r'[^\d.]', '', price_str)
    try:
        return float(numeric)
    except:
        return 0

def extract_venue_from_listings(listings):
    """Extract venue name from listing text"""
    venues = []
    for listing in listings:
        text = listing.get('text', '')
        title = listing.get('title', '')
        
        # Look for venue patterns in text and title
        combined_text = f"{text} {title}".upper()
        
        if 'MEXICO CITY' in combined_text or 'AZTECA' in combined_text:
            venues.append('Mexico City')
        elif 'TORONTO' in combined_text:
            venues.append('Toronto')
        elif 'NEW YORK' in combined_text:
            venues.append('New York')
        elif 'KANSAS CITY' in combined_text:
            venues.append('Kansas City')
        elif 'MIAMI' in combined_text:
            venues.append('Miami')
        elif 'ATLANTA' in combined_text:
            venues.append('Atlanta')
        elif 'HOUSTON' in combined_text:
            venues.append('Houston')
        elif 'SEATTLE' in combined_text:
            venues.append('Seattle')
        elif 'PHILADELPHIA' in combined_text:
            venues.append('Philadelphia')
        elif 'VANCOUVER' in combined_text:
            venues.append('Vancouver')
        elif 'FOXBOROUGH' in combined_text or 'GILLETTE' in combined_text:
            venues.append('Foxborough')
        elif 'INGLEWOOD' in combined_text or 'SOFI' in combined_text:
            venues.append('Inglewood')
        elif 'ARLINGTON' in combined_text:
            venues.append('Arlington')
        elif 'SANTA CLARA' in combined_text:
            venues.append('Santa Clara')
        elif 'GUADALUPE' in combined_text:
            venues.append('Guadalupe')
        elif 'ZAPOPAN' in combined_text:
            venues.append('Zapopan')
    
    # Return most common venue or 'Unknown'
    if venues:
        return max(set(venues), key=venues.count)
    return 'Unknown'

def get_venue_country(venue):
    """Get country for each venue"""
    usa_venues = [
        "Inglewood", "Santa Clara", "Seattle", "Foxborough", "East Rutherford", 
        "Philadelphia", "Miami Gardens", "Atlanta", "Houston", "Kansas City", 
        "Arlington", "Orlando", "Nashville", "Cincinnati", "Denver", "Boston"
    ]
    canada_venues = ["Toronto", "Vancouver"]
    mexico_venues = ["Mexico City", "Zapopan", "Guadalupe", "Monterrey"]
    
    if venue in usa_venues:
        return "USA"
    elif venue in canada_venues:
        return "Canada"
    elif venue in mexico_venues:
        return "Mexico"
    else:
        return "USA"  # Default for any unknown venues

def get_match_schedule():
    """FIFA World Cup 2026 complete match schedule data"""
    return {
        # Group Stage - Matchday 1
        1: {"date": "June 11, 2026", "venue": "Mexico City", "stadium": "Estadio Azteca", "stage": "Group A"},
        2: {"date": "June 11, 2026", "venue": "Zapopan", "stadium": "Estadio Akron", "stage": "Group A"},
        3: {"date": "June 12, 2026", "venue": "Toronto", "stadium": "BMO Field", "stage": "Group B"},
        4: {"date": "June 12, 2026", "venue": "Inglewood", "stadium": "SoFi Stadium", "stage": "Group D"},
        5: {"date": "June 13, 2026", "venue": "Foxborough", "stadium": "Gillette Stadium", "stage": "Group C"},
        6: {"date": "June 13, 2026", "venue": "Vancouver", "stadium": "BC Place", "stage": "Group D"},
        7: {"date": "June 13, 2026", "venue": "East Rutherford", "stadium": "MetLife Stadium", "stage": "Group C"},
        8: {"date": "June 13, 2026", "venue": "Santa Clara", "stadium": "Levi's Stadium", "stage": "Group B"},
        9: {"date": "June 14, 2026", "venue": "Philadelphia", "stadium": "Lincoln Financial Field", "stage": "Group E"},
        10: {"date": "June 14, 2026", "venue": "Houston", "stadium": "NRG Stadium", "stage": "Group E"},
        11: {"date": "June 14, 2026", "venue": "Arlington", "stadium": "AT&T Stadium", "stage": "Group F"},
        12: {"date": "June 14, 2026", "venue": "Guadalupe", "stadium": "Estadio BBVA", "stage": "Group F"},
        13: {"date": "June 15, 2026", "venue": "Miami Gardens", "stadium": "Hard Rock Stadium", "stage": "Group H"},
        14: {"date": "June 15, 2026", "venue": "Atlanta", "stadium": "Mercedes-Benz Stadium", "stage": "Group H"},
        15: {"date": "June 15, 2026", "venue": "Inglewood", "stadium": "SoFi Stadium", "stage": "Group G"},
        16: {"date": "June 15, 2026", "venue": "Seattle", "stadium": "Lumen Field", "stage": "Group G"},
        17: {"date": "June 16, 2026", "venue": "East Rutherford", "stadium": "MetLife Stadium", "stage": "Group I"},
        18: {"date": "June 16, 2026", "venue": "Foxborough", "stadium": "Gillette Stadium", "stage": "Group I"},
        19: {"date": "June 16, 2026", "venue": "Kansas City", "stadium": "Arrowhead Stadium", "stage": "Group J"},
        20: {"date": "June 16, 2026", "venue": "Santa Clara", "stadium": "Levi's Stadium", "stage": "Group J"},
        21: {"date": "June 17, 2026", "venue": "Toronto", "stadium": "BMO Field", "stage": "Group L"},
        22: {"date": "June 17, 2026", "venue": "Arlington", "stadium": "AT&T Stadium", "stage": "Group L"},
        23: {"date": "June 17, 2026", "venue": "Houston", "stadium": "NRG Stadium", "stage": "Group K"},
        24: {"date": "June 17, 2026", "venue": "Mexico City", "stadium": "Estadio Azteca", "stage": "Group K"},
        
        # Group Stage - Matchday 2
        25: {"date": "June 18, 2026", "venue": "Atlanta", "stadium": "Mercedes-Benz Stadium", "stage": "Group A"},
        26: {"date": "June 18, 2026", "venue": "Inglewood", "stadium": "SoFi Stadium", "stage": "Group B"},
        27: {"date": "June 18, 2026", "venue": "Vancouver", "stadium": "BC Place", "stage": "Group B"},
        28: {"date": "June 18, 2026", "venue": "Zapopan", "stadium": "Estadio Akron", "stage": "Group A"},
        29: {"date": "June 19, 2026", "venue": "Philadelphia", "stadium": "Lincoln Financial Field", "stage": "Group C"},
        30: {"date": "June 19, 2026", "venue": "Foxborough", "stadium": "Gillette Stadium", "stage": "Group C"},
        31: {"date": "June 19, 2026", "venue": "Santa Clara", "stadium": "Levi's Stadium", "stage": "Group D"},
        32: {"date": "June 19, 2026", "venue": "Seattle", "stadium": "Lumen Field", "stage": "Group D"},
        33: {"date": "June 20, 2026", "venue": "Toronto", "stadium": "BMO Field", "stage": "Group E"},
        34: {"date": "June 20, 2026", "venue": "Kansas City", "stadium": "Arrowhead Stadium", "stage": "Group E"},
        35: {"date": "June 20, 2026", "venue": "Houston", "stadium": "NRG Stadium", "stage": "Group F"},
        36: {"date": "June 20, 2026", "venue": "Guadalupe", "stadium": "Estadio BBVA", "stage": "Group F"},
        37: {"date": "June 21, 2026", "venue": "Miami Gardens", "stadium": "Hard Rock Stadium", "stage": "Group H"},
        38: {"date": "June 21, 2026", "venue": "Atlanta", "stadium": "Mercedes-Benz Stadium", "stage": "Group H"},
        39: {"date": "June 21, 2026", "venue": "Inglewood", "stadium": "SoFi Stadium", "stage": "Group G"},
        40: {"date": "June 21, 2026", "venue": "Vancouver", "stadium": "BC Place", "stage": "Group G"},
        41: {"date": "June 22, 2026", "venue": "East Rutherford", "stadium": "MetLife Stadium", "stage": "Group I"},
        42: {"date": "June 22, 2026", "venue": "Philadelphia", "stadium": "Lincoln Financial Field", "stage": "Group I"},
        43: {"date": "June 22, 2026", "venue": "Arlington", "stadium": "AT&T Stadium", "stage": "Group J"},
        44: {"date": "June 22, 2026", "venue": "Santa Clara", "stadium": "Levi's Stadium", "stage": "Group J"},
        45: {"date": "June 23, 2026", "venue": "Foxborough", "stadium": "Gillette Stadium", "stage": "Group L"},
        46: {"date": "June 23, 2026", "venue": "Toronto", "stadium": "BMO Field", "stage": "Group L"},
        47: {"date": "June 23, 2026", "venue": "Houston", "stadium": "NRG Stadium", "stage": "Group K"},
        48: {"date": "June 23, 2026", "venue": "Zapopan", "stadium": "Estadio Akron", "stage": "Group K"},
        
        # Group Stage - Matchday 3
        49: {"date": "June 24, 2026", "venue": "Miami Gardens", "stadium": "Hard Rock Stadium", "stage": "Group C"},
        50: {"date": "June 24, 2026", "venue": "Atlanta", "stadium": "Mercedes-Benz Stadium", "stage": "Group C"},
        51: {"date": "June 24, 2026", "venue": "Vancouver", "stadium": "BC Place", "stage": "Group B"},
        52: {"date": "June 24, 2026", "venue": "Seattle", "stadium": "Lumen Field", "stage": "Group B"},
        53: {"date": "June 24, 2026", "venue": "Mexico City", "stadium": "Estadio Azteca", "stage": "Group A"},
        54: {"date": "June 24, 2026", "venue": "Guadalupe", "stadium": "Estadio BBVA", "stage": "Group A"},
        55: {"date": "June 25, 2026", "venue": "Philadelphia", "stadium": "Lincoln Financial Field", "stage": "Group E"},
        56: {"date": "June 25, 2026", "venue": "East Rutherford", "stadium": "MetLife Stadium", "stage": "Group E"},
        57: {"date": "June 25, 2026", "venue": "Arlington", "stadium": "AT&T Stadium", "stage": "Group F"},
        58: {"date": "June 25, 2026", "venue": "Kansas City", "stadium": "Arrowhead Stadium", "stage": "Group F"},
        59: {"date": "June 25, 2026", "venue": "Inglewood", "stadium": "SoFi Stadium", "stage": "Group D"},
        60: {"date": "June 25, 2026", "venue": "Santa Clara", "stadium": "Levi's Stadium", "stage": "Group D"},
        61: {"date": "June 26, 2026", "venue": "Foxborough", "stadium": "Gillette Stadium", "stage": "Group I"},
        62: {"date": "June 26, 2026", "venue": "Toronto", "stadium": "BMO Field", "stage": "Group I"},
        63: {"date": "June 26, 2026", "venue": "Seattle", "stadium": "Lumen Field", "stage": "Group G"},
        64: {"date": "June 26, 2026", "venue": "Vancouver", "stadium": "BC Place", "stage": "Group G"},
        65: {"date": "June 26, 2026", "venue": "Houston", "stadium": "NRG Stadium", "stage": "Group H"},
        66: {"date": "June 26, 2026", "venue": "Zapopan", "stadium": "Estadio Akron", "stage": "Group H"},
        67: {"date": "June 27, 2026", "venue": "East Rutherford", "stadium": "MetLife Stadium", "stage": "Group L"},
        68: {"date": "June 27, 2026", "venue": "Philadelphia", "stadium": "Lincoln Financial Field", "stage": "Group L"},
        69: {"date": "June 27, 2026", "venue": "Kansas City", "stadium": "Arrowhead Stadium", "stage": "Group J"},
        70: {"date": "June 27, 2026", "venue": "Arlington", "stadium": "AT&T Stadium", "stage": "Group J"},
        71: {"date": "June 27, 2026", "venue": "Miami Gardens", "stadium": "Hard Rock Stadium", "stage": "Group K"},
        72: {"date": "June 27, 2026", "venue": "Atlanta", "stadium": "Mercedes-Benz Stadium", "stage": "Group K"},
        
        # Round of 32
        73: {"date": "June 28, 2026", "venue": "Inglewood", "stadium": "SoFi Stadium", "stage": "Round of 32"},
        74: {"date": "June 29, 2026", "venue": "Foxborough", "stadium": "Gillette Stadium", "stage": "Round of 32"},
        75: {"date": "June 29, 2026", "venue": "Guadalupe", "stadium": "Estadio BBVA", "stage": "Round of 32"},
        76: {"date": "June 29, 2026", "venue": "Houston", "stadium": "NRG Stadium", "stage": "Round of 32"},
        77: {"date": "June 30, 2026", "venue": "East Rutherford", "stadium": "MetLife Stadium", "stage": "Round of 32"},
        78: {"date": "June 30, 2026", "venue": "Arlington", "stadium": "AT&T Stadium", "stage": "Round of 32"},
        79: {"date": "June 30, 2026", "venue": "Mexico City", "stadium": "Estadio Azteca", "stage": "Round of 32"},
        80: {"date": "July 1, 2026", "venue": "Atlanta", "stadium": "Mercedes-Benz Stadium", "stage": "Round of 32"},
        81: {"date": "July 1, 2026", "venue": "Santa Clara", "stadium": "Levi's Stadium", "stage": "Round of 32"},
        82: {"date": "July 1, 2026", "venue": "Seattle", "stadium": "Lumen Field", "stage": "Round of 32"},
        83: {"date": "July 2, 2026", "venue": "Toronto", "stadium": "BMO Field", "stage": "Round of 32"},
        84: {"date": "July 2, 2026", "venue": "Inglewood", "stadium": "SoFi Stadium", "stage": "Round of 32"},
        85: {"date": "July 2, 2026", "venue": "Vancouver", "stadium": "BC Place", "stage": "Round of 32"},
        86: {"date": "July 3, 2026", "venue": "Miami Gardens", "stadium": "Hard Rock Stadium", "stage": "Round of 32"},
        87: {"date": "July 3, 2026", "venue": "Kansas City", "stadium": "Arrowhead Stadium", "stage": "Round of 32"},
        88: {"date": "July 3, 2026", "venue": "Arlington", "stadium": "AT&T Stadium", "stage": "Round of 32"},
        
        # Round of 16
        89: {"date": "July 4, 2026", "venue": "Philadelphia", "stadium": "Lincoln Financial Field", "stage": "Round of 16"},
        90: {"date": "July 4, 2026", "venue": "Houston", "stadium": "NRG Stadium", "stage": "Round of 16"},
        91: {"date": "July 5, 2026", "venue": "East Rutherford", "stadium": "MetLife Stadium", "stage": "Round of 16"},
        92: {"date": "July 5, 2026", "venue": "Mexico City", "stadium": "Estadio Azteca", "stage": "Round of 16"},
        93: {"date": "July 6, 2026", "venue": "Arlington", "stadium": "AT&T Stadium", "stage": "Round of 16"},
        94: {"date": "July 6, 2026", "venue": "Seattle", "stadium": "Lumen Field", "stage": "Round of 16"},
        95: {"date": "July 7, 2026", "venue": "Atlanta", "stadium": "Mercedes-Benz Stadium", "stage": "Round of 16"},
        96: {"date": "July 7, 2026", "venue": "Vancouver", "stadium": "BC Place", "stage": "Round of 16"},
        
        # Quarterfinals
        97: {"date": "July 9, 2026", "venue": "Foxborough", "stadium": "Gillette Stadium", "stage": "Quarterfinal"},
        98: {"date": "July 10, 2026", "venue": "Inglewood", "stadium": "SoFi Stadium", "stage": "Quarterfinal"},
        99: {"date": "July 11, 2026", "venue": "Miami Gardens", "stadium": "Hard Rock Stadium", "stage": "Quarterfinal"},
        100: {"date": "July 11, 2026", "venue": "Kansas City", "stadium": "Arrowhead Stadium", "stage": "Quarterfinal"},
        
        # Semifinals
        101: {"date": "July 14, 2026", "venue": "Arlington", "stadium": "AT&T Stadium", "stage": "Semifinal"},
        102: {"date": "July 15, 2026", "venue": "Atlanta", "stadium": "Mercedes-Benz Stadium", "stage": "Semifinal"},
        
        # Third Place Playoff
        103: {"date": "July 18, 2026", "venue": "Miami Gardens", "stadium": "Hard Rock Stadium", "stage": "3rd Place"},
        
        # Final
        104: {"date": "July 19, 2026", "venue": "East Rutherford", "stadium": "MetLife Stadium", "stage": "Final"}
    }

def create_website():
    """Create the FIFA marketplace website"""
    
    data_dir = "fifa_marketplace_data"
    matches = []
    
    # Get match schedule data
    schedule = get_match_schedule()
    
    # Parse all JSON files
    for filename in sorted(os.listdir(data_dir)):
        if filename.startswith('m') and filename.endswith('.json') and filename != 'completion_summary.json':
            match_num = int(filename[1:-5])  # Extract number from m1.json -> 1
            
            with open(os.path.join(data_dir, filename), 'r') as f:
                data = json.load(f)
            
            if data.get('success') and data.get('listings'):
                listings = data['listings']
                
                # Filter out "NO LONGER VALID" listings
                valid_listings = []
                for listing in listings:
                    title = listing.get('title', '').upper()
                    text = listing.get('text', '').upper()
                    
                    # Skip if "NO LONGER VALID" appears in title or text
                    if 'NO LONGER VALID' not in title and 'NO LONGER VALID' not in text:
                        valid_listings.append(listing)
                
                # Extract prices from valid listings only
                prices = [parse_price(listing.get('price', '')) for listing in valid_listings]
                valid_prices = [p for p in prices if p > 0]
                
                if valid_prices:
                    lowest_price = min(valid_prices)
                    highest_price = max(valid_prices)
                    
                    # Get venue info from valid listings
                    extracted_venue = extract_venue_from_listings(valid_listings)
                    
                    # Use schedule data if available, otherwise use extracted
                    match_info = schedule.get(match_num, {})
                    venue = match_info.get('venue', extracted_venue)
                    date = match_info.get('date', 'TBD')
                    stadium = match_info.get('stadium', 'TBD')
                    stage = match_info.get('stage', 'Unknown')
                    
                    matches.append({
                        'match_num': match_num,
                        'date': date,
                        'venue': venue,
                        'stadium': stadium,
                        'stage': stage,
                        'marketplace_url': data['url'],
                        'lowest_price': lowest_price,
                        'highest_price': highest_price,
                        'listings_count': len(valid_listings),
                        'total_listings': len(listings),
                        'invalid_listings': len(listings) - len(valid_listings)
                    })
    
    # Sort by match number
    matches.sort(key=lambda x: x['match_num'])
    
    # Create HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FIFA World Cup 2026 Marketplace</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 10px;
        }}
        
        @media (max-width: 480px) {{
            body {{
                padding: 5px;
            }}
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                border-radius: 15px;
            }}
        }}
        
        @media (max-width: 480px) {{
            .container {{
                border-radius: 10px;
                margin: 0 5px;
            }}
        }}
        
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 3rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }}
        
        @media (max-width: 768px) {{
            .header {{
                padding: 30px 20px;
            }}
            
            .header h1 {{
                font-size: 2.2rem;
            }}
        }}
        
        @media (max-width: 480px) {{
            .header {{
                padding: 25px 15px;
            }}
            
            .header h1 {{
                font-size: 1.8rem;
            }}
        }}
        
        .header p {{
            font-size: 1.2rem;
            opacity: 0.9;
        }}
        
        .last-updated {{
            font-size: 0.9rem !important;
            color: #888 !important;
            font-style: italic;
            opacity: 0.8 !important;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        
        @media (max-width: 768px) {{
            .stats {{
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 15px;
                padding: 20px;
            }}
        }}
        
        @media (max-width: 480px) {{
            .stats {{
                grid-template-columns: 1fr 1fr;
                gap: 10px;
                padding: 15px;
            }}
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-number {{
            font-size: 2.5rem;
            font-weight: bold;
            color: #2a5298;
        }}
        
        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}
        
        .table-container {{
            padding: 30px;
            overflow-x: auto;
        }}
        
        @media (max-width: 768px) {{
            .table-container {{
                padding: 15px;
            }}
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }}
        
        @media (min-width: 769px) {{
            table {{
                min-width: 800px;
            }}
        }}
        
        @media (max-width: 768px) {{
            table {{
                font-size: 0.85rem;
                border-radius: 10px;
            }}
            
            /* Hide less important columns on tablet */
            .hide-tablet {{
                display: none;
            }}
        }}
        
        @media (max-width: 480px) {{
            table {{
                font-size: 0.75rem;
                border-radius: 8px;
            }}
            
            /* Hide more columns on mobile */
            .hide-mobile {{
                display: none;
            }}
        }}
        
        th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 10px;
            font-weight: 600;
            text-align: left;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            cursor: pointer;
            user-select: none;
            position: relative;
        }}
        
        @media (max-width: 768px) {{
            th {{
                padding: 10px 6px;
                font-size: 0.75rem;
                letter-spacing: 0.3px;
            }}
        }}
        
        @media (max-width: 480px) {{
            th {{
                padding: 8px 4px;
                font-size: 0.65rem;
                letter-spacing: 0.2px;
            }}
        }}
        
        th:hover {{
            background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
        }}
        
        th.sortable::after {{
            content: ' ⇅';
            font-size: 10px;
            margin-left: 8px;
            opacity: 0.6;
        }}
        
        th.sort-asc::after {{
            content: ' ▲';
            font-size: 8px;
            margin-left: 8px;
            opacity: 1;
        }}
        
        th.sort-desc::after {{
            content: ' ▼';
            font-size: 8px;
            margin-left: 8px;
            opacity: 1;
        }}
        
        td {{
            padding: 12px 8px;
            border-bottom: 1px solid #eee;
            transition: background-color 0.3s ease;
            word-wrap: break-word;
            max-width: 150px;
        }}
        
        @media (max-width: 768px) {{
            td {{
                padding: 8px 5px;
                font-size: 0.85rem;
                max-width: 120px;
            }}
        }}
        
        @media (max-width: 480px) {{
            td {{
                padding: 6px 3px;
                font-size: 0.75rem;
                max-width: 100px;
            }}
        }}
        
        tr:hover td {{
            background-color: #f8f9ff;
        }}
        
        tr:nth-child(even) td {{
            background-color: #fafafa;
        }}
        
        .match-num {{
            font-weight: bold;
            color: #2a5298;
            font-size: 1.1rem;
        }}
        
        .venue {{
            font-weight: 600;
            color: #333;
        }}
        
        .price {{
            font-weight: bold;
            color: #28a745;
        }}
        
        .price.high {{
            color: #dc3545;
        }}
        
        .marketplace-link {{
            color: #007bff;
            text-decoration: none;
            padding: 6px 12px;
            background: #e3f2fd;
            border-radius: 15px;
            font-size: 0.8rem;
            transition: all 0.3s ease;
            display: inline-block;
            white-space: nowrap;
        }}
        
        .marketplace-link:hover {{
            background: #007bff;
            color: white;
        }}
        
        @media (max-width: 768px) {{
            .marketplace-link {{
                padding: 4px 8px;
                font-size: 0.7rem;
                border-radius: 10px;
            }}
        }}
        
        @media (max-width: 480px) {{
            .marketplace-link {{
                padding: 3px 6px;
                font-size: 0.65rem;
                border-radius: 8px;
            }}
        }}
        
        .date {{
            color: #666;
            font-weight: 500;
        }}
        
        .final-match {{
            background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%) !important;
            font-weight: bold;
        }}
        
        .final-match td {{
            background: rgba(255, 215, 0, 0.1) !important;
        }}
        
        .semifinal-match td {{
            background: rgba(255, 165, 0, 0.1) !important;
        }}
        
        .knockout-match td {{
            background: rgba(30, 144, 255, 0.05) !important;
        }}
        
        .stage {{
            font-weight: 600;
            color: #2a5298;
            text-transform: uppercase;
            font-size: 0.9rem;
        }}
        
        /* Mobile-specific venue info */
        .venue-mobile-info {{
            display: none;
            font-size: 0.7rem;
            color: #666;
            margin-top: 2px;
        }}
        
        @media (max-width: 480px) {{
            .venue-mobile-info {{
                display: block;
            }}
        }}
        
        .footer {{
            background: #2a5298;
            color: white;
            text-align: center;
            padding: 30px;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2rem;
            }}
            
            .stats {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            th, td {{
                padding: 10px 8px;
                font-size: 0.9rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
                <div class="header">
            <p style="text-align: center; margin: 0 0 20px 0;"><a href="https://coff.ee/rahulxc" target="_blank" style="color: #ffffff; text-decoration: none; font-weight: 600; opacity: 0.9;">☕ Support this project: coff.ee/rahulxc</a></p>
            <h1>🏆 FIFA World Cup 2026 Marketplace</h1>
            <p class="subtitle">Official FIFA Collect RTB (Right to Buy) Collectibles • Real-time marketplace data</p>
            <p class="last-updated">Last updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(matches)}</div>
                <div class="stat-label">Total Matches</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">${min(m['lowest_price'] for m in matches if m['lowest_price'] > 0):,.0f}</div>
                <div class="stat-label">Lowest Price</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">${max(m['highest_price'] for m in matches):,.0f}</div>
                <div class="stat-label">Highest Price</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{sum(m['listings_count'] for m in matches):,}</div>
                <div class="stat-label">Valid Listings</div>
            </div>
        </div>
        
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th class="sortable" onclick="sortTable(0)">Match #</th>
                        <th class="sortable hide-mobile" onclick="sortTable(1)">Date</th>
                        <th class="sortable hide-mobile" onclick="sortTable(2)">Stage</th>
                        <th class="sortable" onclick="sortTable(3)">Venue</th>
                        <th class="sortable hide-tablet" onclick="sortTable(4)">Country</th>
                        <th class="sortable hide-tablet" onclick="sortTable(5)">Stadium</th>
                        <th class="sortable hide-mobile" onclick="sortTable(6)">Listings</th>
                        <th class="sortable" onclick="sortTable(7)">Low Price</th>
                        <th class="sortable hide-mobile" onclick="sortTable(8)">High Price</th>
                        <th class="sortable" onclick="sortTable(9)">Link</th>
                    </tr>
                </thead>
                <tbody>
"""
    
    # Add table rows
    for match in matches:
        is_final = match['match_num'] == 104
        is_semifinal = match['stage'] == 'Semifinal'
        is_knockout = match['stage'] in ['Round of 32', 'Round of 16', 'Quarterfinal', 'Semifinal', '3rd Place', 'Final']
        
        row_class = ''
        if is_final:
            row_class = 'final-match'
        elif is_semifinal:
            row_class = 'semifinal-match'
        elif is_knockout:
            row_class = 'knockout-match'
        
        html_content += f"""
                    <tr class="{row_class}">
                        <td class="match-num">M{match['match_num']}</td>
                        <td class="date hide-mobile">{match['date']}</td>
                        <td class="stage hide-mobile">{match['stage']}</td>
                        <td class="venue">{match['venue']}<div class="venue-mobile-info">{match['date']} • {match['stage']}</div></td>
                        <td class="country hide-tablet">{get_venue_country(match['venue'])}</td>
                        <td class="hide-tablet">{match['stadium']}</td>
                        <td class="listings-count hide-mobile">{match['listings_count']}</td>
                        <td class="price">${match['lowest_price']:,.0f}</td>
                        <td class="price high hide-mobile">${match['highest_price']:,.0f}</td>
                        <td><a href="{match['marketplace_url']}" target="_blank" class="marketplace-link">View</a></td>
                    </tr>
"""
    
    html_content += f"""
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>Data scraped from FIFA Collect Marketplace • Last updated: {datetime.now().strftime('%B %d, %Y')}</p>
            <p>RTB = Right to Buy • Collectibles grant priority access to purchase actual match tickets</p>
        </div>
    </div>
    
    <script>
        let sortDirection = {{}};
        
        function sortTable(columnIndex) {{
            const table = document.querySelector('table');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            const headers = table.querySelectorAll('th');
            
            // Clear previous sorting indicators
            headers.forEach(header => {{
                header.classList.remove('sort-asc', 'sort-desc');
            }});
            
            // Determine sort direction
            const currentDirection = sortDirection[columnIndex] || 'asc';
            const newDirection = currentDirection === 'asc' ? 'desc' : 'asc';
            sortDirection[columnIndex] = newDirection;
            
            // Add sorting indicator
            headers[columnIndex].classList.add(`sort-${{newDirection}}`);
            
            // Sort rows
            rows.sort((a, b) => {{
                const aVal = getCellValue(a, columnIndex);
                const bVal = getCellValue(b, columnIndex);
                
                if (columnIndex === 0 || columnIndex === 6 || columnIndex === 7 || columnIndex === 8) {{
                    // Numeric columns (Match #, Valid Listings, Prices)
                    const aNum = parseFloat(aVal.replace(/[^0-9.-]/g, '')) || 0;
                    const bNum = parseFloat(bVal.replace(/[^0-9.-]/g, '')) || 0;
                    return newDirection === 'asc' ? aNum - bNum : bNum - aNum;
                }} else {{
                    // Text columns
                    return newDirection === 'asc' ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
                }}
            }});
            
            // Re-append sorted rows
            rows.forEach(row => tbody.appendChild(row));
        }}
        
        function getCellValue(row, index) {{
            return row.cells[index].textContent.trim();
        }}
    </script>
</body>
</html>
"""
    
    # Save the HTML file
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Also save as the original filename for backwards compatibility
    with open('fifa_world_cup_2026_marketplace.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Website created: index.html (GitHub Pages ready)")
    print(f"📊 {len(matches)} matches processed")
    print(f"💰 Price range: ${min(m['lowest_price'] for m in matches if m['lowest_price'] > 0):,.0f} - ${max(m['highest_price'] for m in matches):,.0f}")

if __name__ == "__main__":
    create_website()
