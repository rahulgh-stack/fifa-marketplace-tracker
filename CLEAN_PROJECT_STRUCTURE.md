# FIFA Marketplace Project - Clean Structure

## Essential Files (Keep These)

### Core Scripts
- `fifa_scraper.py` - Main scraper script (NEW - replaces all old scrapers)
- `create_website.py` - Website generator
- `requirements.txt` - Python dependencies

### Data & Output
- `fifa_marketplace_data/` - Match data directory (CONSTANT NAME)
  - `m1.json` to `m104.json` - Individual match marketplace data
- `index.html` - Generated website (GitHub Pages)
- `README.md` - Project documentation

## Files to Delete (Temporary/Redundant)

### Old Scraper Scripts (Replace with fifa_scraper.py)
- `final_scraper.py`
- `complete_remaining.py`
- `retry_failed.py`
- `retry_failed_exact.py`
- `retry_failed_matches.py`
- `gentle_retry.py`
- `quick_retry.py`
- `update_selected_matches.py`
- `update_m104_only.py`
- `update_m75.py`

### Temporary Files
- `update_summary.json`
- `fifa_world_cup_2026_marketplace.html` (old filename)
- `fifa_complete_20250723_115019/` (old data directory)

## New Usage

### Scrape All Matches
```bash
python3 fifa_scraper.py
```

### Scrape Specific Matches
```bash
python3 fifa_scraper.py 1 104 7 17 24
```

### Generate Website
```bash
python3 create_website.py
```

## Key Improvements

1. **Constant folder name**: `fifa_marketplace_data` (no more timestamps)
2. **Robust error handling**: Only updates JSON if scraping succeeds
3. **Preserve old data**: Failed scrapes don't overwrite existing data
4. **Clean structure**: One main scraper instead of multiple scripts
5. **Coffee link**: Permanently embedded in website template

## File Sizes (Approximate)
- Each match JSON: 2-8KB
- Total data directory: ~500KB
- Generated website: ~200KB