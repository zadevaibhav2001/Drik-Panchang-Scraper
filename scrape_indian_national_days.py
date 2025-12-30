#!/usr/bin/env python3
"""
Indian National Days Scraper
Scrapes important days from Career Power website for all months
"""

import requests
from bs4 import BeautifulSoup
import csv
import json
import time
from datetime import datetime
import re

class IndianNationalDaysScraper:
    def __init__(self):
        self.base_url = "https://www.careerpower.in/blog/important-days-in-{}"
        self.months = [
            'january', 'february', 'march', 'april', 'may', 'june',
            'july', 'august', 'september', 'october', 'november', 'december'
        ]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.all_events = {}
        
    def scrape_month(self, month):
        """Scrape events for a specific month"""
        url = self.base_url.format(month)
        print(f"Scraping {month.capitalize()}...")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            events = []
            
            # Find the table with events
            tables = soup.find_all('table')
            
            for table in tables:
                rows = table.find_all('tr')
                
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 2:
                        date_cell = cells[0].get_text(strip=True)
                        event_cell = cells[1].get_text(separator=' ', strip=True)
                        
                        # Skip header rows
                        if 'Dates' in date_cell or 'Days' in date_cell:
                            continue
                            
                        # Clean up the date and event text
                        if date_cell and event_cell and any(char.isdigit() for char in date_cell):
                            # Handle multiple events in one cell (separated by line breaks)
                            event_parts = event_cell.replace('\n', ' ').split('  ')
                            event_parts = [part.strip() for part in event_parts if part.strip()]
                            
                            for event_part in event_parts:
                                if event_part and len(event_part) > 3:  # Filter out very short strings
                                    events.append({
                                        'date': date_cell,
                                        'event': event_part,
                                        'month': month.capitalize()
                                    })
            
            # Also try to find events in paragraph format
            paragraphs = soup.find_all(['p', 'h3', 'h4'])
            for para in paragraphs:
                text = para.get_text(strip=True)
                # Look for patterns like "World Braille Day- 4th January 2025"
                if re.search(r'\d{1,2}(st|nd|rd|th)\s+' + month, text, re.IGNORECASE):
                    # Extract event name and date
                    match = re.search(r'(.+?)-\s*(\d{1,2}(st|nd|rd|th)\s+' + month + r')', text, re.IGNORECASE)
                    if match:
                        event_name = match.group(1).strip()
                        date_str = match.group(2).strip()
                        
                        if event_name and len(event_name) > 3:
                            events.append({
                                'date': date_str,
                                'event': event_name,
                                'month': month.capitalize()
                            })
            
            print(f"Found {len(events)} events for {month.capitalize()}")
            return events
            
        except requests.RequestException as e:
            print(f"Error scraping {month}: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error for {month}: {e}")
            return []
    
    def scrape_all_months(self):
        """Scrape events for all months"""
        for month in self.months:
            events = self.scrape_month(month)
            self.all_events[month] = events
            
            # Be respectful to the server
            time.sleep(2)
    
    def clean_and_deduplicate(self):
        """Clean up and remove duplicate events"""
        for month in self.all_events:
            events = self.all_events[month]
            cleaned_events = []
            seen_events = set()
            
            for event in events:
                # Clean up the event text
                event_text = re.sub(r'\s+', ' ', event['event']).strip()
                event_text = re.sub(r'[^\w\s\-\(\)&]', '', event_text)
                
                # Create a key for deduplication
                key = (event['date'].lower(), event_text.lower())
                
                if key not in seen_events and len(event_text) > 3:
                    seen_events.add(key)
                    cleaned_events.append({
                        'date': event['date'],
                        'event': event_text,
                        'month': event['month']
                    })
            
            self.all_events[month] = cleaned_events
    
    def save_to_csv(self, filename='indian_national_days.csv'):
        """Save events to CSV file"""
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Month', 'Date', 'Event']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for month in self.months:
                events = self.all_events.get(month, [])
                for event in events:
                    writer.writerow({
                        'Month': event['month'],
                        'Date': event['date'],
                        'Event': event['event']
                    })
        
        print(f"Data saved to {filename}")
    
    def save_to_json(self, filename='indian_national_days.json'):
        """Save events to JSON file"""
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(self.all_events, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"Data saved to {filename}")
    
    def generate_html_report(self, filename='indian_national_days.html'):
        """Generate an HTML report"""
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Indian National Days - Complete Calendar</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #ff6b6b, #ee5a24);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .content {
            padding: 30px;
        }
        .month-section {
            margin-bottom: 40px;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
        }
        .month-header {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 15px 20px;
            font-size: 1.5em;
            font-weight: bold;
        }
        .events-table {
            width: 100%;
            border-collapse: collapse;
        }
        .events-table th {
            background: #f8f9fa;
            padding: 12px;
            text-align: left;
            border-bottom: 2px solid #dee2e6;
            font-weight: bold;
        }
        .events-table td {
            padding: 12px;
            border-bottom: 1px solid #dee2e6;
        }
        .events-table tr:hover {
            background: #f8f9fa;
        }
        .date-cell {
            font-weight: bold;
            color: #007cba;
            white-space: nowrap;
            width: 150px;
        }
        .event-cell {
            color: #333;
        }
        .stats {
            background: #e8f5e8;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }
        .stats h3 {
            margin: 0 0 10px 0;
            color: #2e7d32;
        }
        @media (max-width: 768px) {
            body { padding: 10px; }
            .header h1 { font-size: 1.8em; }
            .content { padding: 20px; }
            .events-table { font-size: 14px; }
            .date-cell { width: 120px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🇮🇳 Indian National Days Calendar</h1>
            <p>Complete list of Important Days and Events throughout the year</p>
        </div>
        
        <div class="content">
            <div class="stats">
                <h3>📊 Statistics</h3>
                <p>Total Events: <strong>{total_events}</strong> | Generated on: <strong>{generation_date}</strong></p>
            </div>
            
            {month_sections}
        </div>
    </div>
</body>
</html>
        """
        
        month_sections = ""
        total_events = 0
        
        for month in self.months:
            events = self.all_events.get(month, [])
            total_events += len(events)
            
            if events:
                month_sections += f"""
            <div class="month-section">
                <div class="month-header">{month.capitalize()} ({len(events)} events)</div>
                <table class="events-table">
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Event</th>
                        </tr>
                    </thead>
                    <tbody>
                """
                
                for event in events:
                    month_sections += f"""
                        <tr>
                            <td class="date-cell">{event['date']}</td>
                            <td class="event-cell">{event['event']}</td>
                        </tr>
                    """
                
                month_sections += """
                    </tbody>
                </table>
            </div>
                """
        
        final_html = html_content.format(
            total_events=total_events,
            generation_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            month_sections=month_sections
        )
        
        with open(filename, 'w', encoding='utf-8') as htmlfile:
            htmlfile.write(final_html)
        
        print(f"HTML report saved to {filename}")
    
    def print_summary(self):
        """Print a summary of scraped data"""
        print("\n" + "="*60)
        print("SCRAPING SUMMARY")
        print("="*60)
        
        total_events = 0
        for month in self.months:
            events = self.all_events.get(month, [])
            total_events += len(events)
            print(f"{month.capitalize():12}: {len(events):3} events")
        
        print("-"*60)
        print(f"{'Total':12}: {total_events:3} events")
        print("="*60)

def main():
    scraper = IndianNationalDaysScraper()
    
    print("🇮🇳 Indian National Days Scraper")
    print("=" * 50)
    print("Scraping important days from Career Power website...")
    print()
    
    # Scrape all months
    scraper.scrape_all_months()
    
    # Clean and deduplicate
    print("\nCleaning and deduplicating data...")
    scraper.clean_and_deduplicate()
    
    # Print summary
    scraper.print_summary()
    
    # Save to different formats
    print("\nSaving data to files...")
    scraper.save_to_csv()
    scraper.save_to_json()
    scraper.generate_html_report()
    
    print("\n✅ Scraping completed successfully!")
    print("\nGenerated files:")
    print("- indian_national_days.csv (CSV format)")
    print("- indian_national_days.json (JSON format)")
    print("- indian_national_days.html (HTML report)")

if __name__ == "__main__":
    main()