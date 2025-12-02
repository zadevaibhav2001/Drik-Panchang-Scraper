import requests
from bs4 import BeautifulSoup

# Scrape the website
url = 'https://www.drikpanchang.com/iskcon/iskcon-event-calendar.html?year=2025'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
response = requests.get(url, headers=headers)
html_content = response.text

# Parse HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Find all elements with class dpEventInfo
event_infos = soup.find_all('div', class_='dpEventInfo')

from collections import defaultdict
from datetime import datetime

# Extract data
events = []
print(f"Found {len(event_infos)} event_infos")

for event_info in event_infos:
    greg_date = event_info.find('div', class_='dpEventGregDate')
    event_name = event_info.find('div', class_='dpEventName dpHinduEventColor')
    
    if greg_date and event_name:
        date_text = greg_date.get_text(strip=True)
        name_text = event_name.get_text(strip=True)
        print(f"Found event: {date_text} - {name_text}")
        events.append({
            'date': date_text,
            'name': name_text
        })

print(f"Total events extracted: {len(events)}")

# Group by month and date
monthly_events = defaultdict(lambda: defaultdict(list))
for event in events:
    try:
        # Parse format like "December 17, 2025, Wednesday"
        date_part = event['date'].split(',')[0] + ', ' + event['date'].split(',')[1].strip()
        date_obj = datetime.strptime(date_part, '%B %d, %Y')
        month = date_obj.strftime('%b')
        day = date_obj.day
        monthly_events[month][day].append(event['name'])
    except Exception as e:
        print(f"Date parsing error for '{event['date']}': {e}")
        continue

print(f"Months found: {list(monthly_events.keys())}")

# Print formatted results
if not monthly_events:
    print("No events found to display")
else:
    month_days = {'Jan': 31, 'Feb': 28, 'Mar': 31, 'Apr': 30, 'May': 31, 'Jun': 30,
                  'Jul': 31, 'Aug': 31, 'Sep': 30, 'Oct': 31, 'Nov': 30, 'Dec': 31}
    
    for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
        if month in monthly_events:
            print(f"{month} Planner\n")
            for day in range(1, month_days[month] + 1):
                if day in monthly_events[month]:
                    event_names = monthly_events[month][day]
                    if len(event_names) == 1:
                        print(f"{day}. {event_names[0]}")
                    else:
                        print(f"{day}. {event_names[0]}")
                        for name in event_names[1:]:
                            print(f"   {name}")
                else:
                    print(f"{day}.")
            print()