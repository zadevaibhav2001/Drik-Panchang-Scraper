# Drik-Panchang-Scraper

A web scraper for ISKCON events from Drik Panchang calendar with GitHub Pages interface, now enhanced with Indian National Days data.

## Features

- Select year and month from dropdowns
- Scrape ISKCON events from drikpanchang.com
- Display events in monthly planner format
- **NEW**: Indian National Days from comprehensive JSON database
- **NEW**: Enhanced calendar mixing with Indian national days
- Client-side JavaScript implementation for GitHub Pages

## Calendar Types

1. **ISKCON Events** - Religious events from Drik Panchang
2. **Indian National Days** - Comprehensive list of national and international days celebrated in India
3. **UN International Days** - United Nations recognized international observances

## Usage

1. Visit the GitHub Pages site
2. Select desired calendar type and year
3. Optionally select a specific month
4. Click "Get Events" to scrape and display results
5. **NEW**: Mix different calendar types by adding Indian National Days or UN days to ISKCON calendar

## Files

- `index.html` - Main web interface with enhanced calendar mixing
- `scrape_panchang.py` - Original Python scraper script
- `scrape_indian_national_days.py` - **NEW**: Python scraper for Indian national days
- `indian_national_days.json` - **NEW**: Comprehensive database of Indian national days
- `_config.yml` - Jekyll configuration for GitHub Pages

## Data Sources

- **ISKCON Events**: drikpanchang.com (scraped dynamically)
- **Indian National Days**: Career Power website (pre-scraped into JSON)
- **UN International Days**: Hardcoded data from UN website

## Setup GitHub Pages

1. Push this repository to GitHub
2. Go to repository Settings > Pages
3. Select "Deploy from a branch" and choose "main"
4. Your site will be available at `https://username.github.io/repository-name`

## Indian National Days Database

The `indian_national_days.json` file contains a comprehensive collection of important days celebrated in India, including:

- National holidays and observances
- International days recognized in India
- Cultural and religious festivals
- Awareness days and campaigns
- Historical commemorations

### Updating Indian National Days

To update the Indian National Days database:

1. Run the scraper: `python3 scrape_indian_national_days.py`
2. This will generate updated `indian_national_days.json`, `indian_national_days.csv`, and `indian_national_days.html` files
3. The web interface automatically uses the JSON file

## Note

The web version uses a CORS proxy (allorigins.win) to bypass browser restrictions when scraping external sites for ISKCON events. Indian National Days are loaded directly from the local JSON file for better performance and reliability.