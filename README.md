# Drik-Panchang-Scraper

A web scraper for ISKCON events from Drik Panchang calendar with GitHub Pages interface.

## Features

- Select year and month from dropdowns
- Scrape ISKCON events from drikpanchang.com
- Display events in monthly planner format
- Client-side JavaScript implementation for GitHub Pages

## Usage

1. Visit the GitHub Pages site
2. Select desired year and optionally a specific month
3. Click "Get Events" to scrape and display results

## Files

- `index.html` - Main web interface
- `scrape_panchang.py` - Original Python scraper script
- `_config.yml` - Jekyll configuration for GitHub Pages

## Setup GitHub Pages

1. Push this repository to GitHub
2. Go to repository Settings > Pages
3. Select "Deploy from a branch" and choose "main"
4. Your site will be available at `https://username.github.io/repository-name`

## Note

The web version uses a CORS proxy (allorigins.win) to bypass browser restrictions when scraping external sites.