import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import re

def scrape_un_days():
    url = 'https://www.un.org/en/observances/list-days-weeks'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all event rows
        events_by_month = defaultdict(list)
        
        # Look for the main content area
        rows = soup.find_all('div', class_='views-row')
        
        print(f"Found {len(rows)} event rows")
        
        for row in rows:
            try:
                # Find title
                title_elem = row.find('span', class_='views-field-title')
                if not title_elem:
                    continue
                    
                title_link = title_elem.find('a')
                if not title_link:
                    continue
                    
                event_name = title_link.get_text(strip=True)
                
                # Find date
                date_elem = row.find('div', class_='views-field-field-event-date-1')
                if not date_elem:
                    continue
                    
                date_span = date_elem.find('span', class_='date-display-single')
                if not date_span:
                    continue
                    
                date_text = date_span.get_text(strip=True)
                
                # Parse date to get month
                try:
                    # Date format is like "04 Jun" or "27 Jan"
                    day, month_abbr = date_text.split()
                    
                    month_map = {
                        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
                    }
                    
                    month_num = month_map.get(month_abbr)
                    if month_num:
                        events_by_month[month_num].append({
                            'date': date_text,
                            'name': event_name
                        })
                        print(f"Added: {date_text} - {event_name}")
                        
                except ValueError:
                    print(f"Could not parse date: {date_text}")
                    continue
                    
            except Exception as e:
                print(f"Error processing row: {e}")
                continue
        
        return events_by_month
        
    except Exception as e:
        print(f"Error scraping UN days: {e}")
        return {}

def format_for_javascript(events_by_month):
    """Format the data for JavaScript object"""
    
    month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    
    print("\n" + "="*50)
    print("JAVASCRIPT FORMAT:")
    print("="*50)
    
    print("const unDaysData = {")
    
    for month_num in range(1, 13):
        if month_num in events_by_month:
            events = events_by_month[month_num]
            # Sort events by day
            events.sort(key=lambda x: int(x['date'].split()[0]))
            
            print(f"    {month_num}: [", end="")
            
            event_strings = []
            for event in events:
                name_escaped = event['name'].replace("'", "\\'")
                event_strings.append(f"{{date: '{event['date']}', name: '{name_escaped}'}}")
            
            print(", ".join(event_strings), end="")
            print("],")
    
    print("};")

def print_summary(events_by_month):
    """Print summary by month"""
    
    month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    
    print("\n" + "="*50)
    print("SUMMARY BY MONTH:")
    print("="*50)
    
    total_events = 0
    
    for month_num in range(1, 13):
        if month_num in events_by_month:
            events = events_by_month[month_num]
            events.sort(key=lambda x: int(x['date'].split()[0]))
            
            print(f"\n{month_names[month_num]} ({len(events)} events):")
            print("-" * 30)
            
            for event in events:
                print(f"  {event['date']} - {event['name']}")
            
            total_events += len(events)
        else:
            print(f"\n{month_names[month_num]} (0 events):")
            print("-" * 30)
    
    print(f"\nTotal events found: {total_events}")

if __name__ == "__main__":
    print("Scraping UN International Days...")
    events = scrape_un_days()
    
    if events:
        print_summary(events)
        format_for_javascript(events)
    else:
        print("No events found or error occurred")