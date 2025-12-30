#!/usr/bin/env python3
"""
ISKCON Maharaj Days Processor
Converts swamisiskcon.csv to JSON format similar to indian_national_days.json
"""

import csv
import json
from datetime import datetime
import re

def parse_date(date_str):
    """Parse various date formats and return month and formatted date"""
    if not date_str or date_str.strip() == '-':
        return None, None
    
    date_str = date_str.strip()
    
    # Handle different date formats
    formats = [
        '%d %B %Y',      # 17 September 1945
        '%d %b %Y',      # 25 Feb 1950
        '%d/%m/%Y',      # 15/3/2002
        '%d-%m-%Y',      # Alternative format
        '%B %d %Y',      # September 17 1945
        '%b %d %Y'       # Feb 25 1950
    ]
    
    for fmt in formats:
        try:
            date_obj = datetime.strptime(date_str, fmt)
            month_name = date_obj.strftime('%B').lower()
            formatted_date = date_obj.strftime('%d %B')
            return month_name, formatted_date
        except ValueError:
            continue
    
    # Manual parsing for edge cases
    try:
        # Handle formats like "15/3/2002"
        if '/' in date_str:
            parts = date_str.split('/')
            if len(parts) == 3:
                day, month, year = parts
                date_obj = datetime(int(year), int(month), int(day))
                month_name = date_obj.strftime('%B').lower()
                formatted_date = date_obj.strftime('%d %B')
                return month_name, formatted_date
    except:
        pass
    
    print(f"Could not parse date: {date_str}")
    return None, None

def process_maharaj_data():
    """Process the CSV file and create JSON structure"""
    maharaj_days = {
        'january': [],
        'february': [],
        'march': [],
        'april': [],
        'may': [],
        'june': [],
        'july': [],
        'august': [],
        'september': [],
        'october': [],
        'november': [],
        'december': []
    }
    
    with open('swamisiskcon.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            maharaj_name = row.get('Maharaj', '').strip()
            appearance_date = row.get('App', '').strip()
            disappearance_date = row.get('Disapp', '').strip()
            
            if not maharaj_name:
                continue
            
            # Process appearance date
            if appearance_date and appearance_date != '-':
                month, formatted_date = parse_date(appearance_date)
                if month and formatted_date:
                    event = {
                        "date": formatted_date,
                        "event": f"{maharaj_name} - Appearance Day",
                        "month": month.capitalize(),
                        "type": "appearance"
                    }
                    maharaj_days[month].append(event)
            
            # Process disappearance date
            if disappearance_date and disappearance_date != '-':
                month, formatted_date = parse_date(disappearance_date)
                if month and formatted_date:
                    event = {
                        "date": formatted_date,
                        "event": f"{maharaj_name} - Disappearance Day",
                        "month": month.capitalize(),
                        "type": "disappearance"
                    }
                    maharaj_days[month].append(event)
    
    # Sort events by date within each month
    for month in maharaj_days:
        maharaj_days[month].sort(key=lambda x: int(x['date'].split()[0]))
    
    return maharaj_days

def save_to_json(data, filename='iskcon_maharaj_days.json'):
    """Save data to JSON file"""
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=2, ensure_ascii=False)
    print(f"Data saved to {filename}")

def generate_summary(data):
    """Generate a summary of the data"""
    print("\n" + "="*60)
    print("ISKCON MAHARAJ DAYS SUMMARY")
    print("="*60)
    
    total_events = 0
    appearance_count = 0
    disappearance_count = 0
    
    for month, events in data.items():
        month_appearances = len([e for e in events if e['type'] == 'appearance'])
        month_disappearances = len([e for e in events if e['type'] == 'disappearance'])
        total_month = len(events)
        
        if total_month > 0:
            print(f"{month.capitalize():12}: {total_month:2} events ({month_appearances} app, {month_disappearances} dis)")
        
        total_events += total_month
        appearance_count += month_appearances
        disappearance_count += month_disappearances
    
    print("-"*60)
    print(f"{'Total':12}: {total_events:2} events ({appearance_count} appearances, {disappearance_count} disappearances)")
    print("="*60)

def generate_html_report(data, filename='iskcon_maharaj_days.html'):
    """Generate an HTML report"""
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ISKCON Maharaj Days Calendar</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #ff9a56 0%, #ff6b35 100%);
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
            background: linear-gradient(135deg, #ff6b35, #f7931e);
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
            background: linear-gradient(135deg, #ff9a56 0%, #ff6b35 100%);
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
            background: #fff5f0;
        }
        .date-cell {
            font-weight: bold;
            color: #ff6b35;
            white-space: nowrap;
            width: 150px;
        }
        .event-cell {
            color: #333;
        }
        .appearance {
            background: #e8f5e8;
        }
        .disappearance {
            background: #fff3cd;
        }
        .stats {
            background: #fff5f0;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }
        .stats h3 {
            margin: 0 0 10px 0;
            color: #ff6b35;
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
            <h1>🕉️ ISKCON Maharaj Days Calendar</h1>
            <p>Appearance and Disappearance Days of ISKCON Spiritual Masters</p>
        </div>
        
        <div class="content">
            <div class="stats">
                <h3>📊 Statistics</h3>
                <p>Total Events: <strong>{total_events}</strong> | Appearances: <strong>{appearances}</strong> | Disappearances: <strong>{disappearances}</strong></p>
                <p>Generated on: <strong>{generation_date}</strong></p>
            </div>
            
            {month_sections}
        </div>
    </div>
</body>
</html>
    """
    
    month_sections = ""
    total_events = 0
    total_appearances = 0
    total_disappearances = 0
    
    month_order = ['january', 'february', 'march', 'april', 'may', 'june',
                   'july', 'august', 'september', 'october', 'november', 'december']
    
    for month in month_order:
        events = data.get(month, [])
        if events:
            appearances = len([e for e in events if e['type'] == 'appearance'])
            disappearances = len([e for e in events if e['type'] == 'disappearance'])
            
            total_events += len(events)
            total_appearances += appearances
            total_disappearances += disappearances
            
            month_sections += f"""
            <div class="month-section">
                <div class="month-header">{month.capitalize()} ({len(events)} events - {appearances} app, {disappearances} dis)</div>
                <table class="events-table">
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Event</th>
                            <th>Type</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            
            for event in events:
                event_type = event['type']
                row_class = 'appearance' if event_type == 'appearance' else 'disappearance'
                type_display = '🎂 Appearance' if event_type == 'appearance' else '🙏 Disappearance'
                
                month_sections += f"""
                    <tr class="{row_class}">
                        <td class="date-cell">{event['date']}</td>
                        <td class="event-cell">{event['event']}</td>
                        <td>{type_display}</td>
                    </tr>
                """
            
            month_sections += """
                    </tbody>
                </table>
            </div>
            """
    
    final_html = html_content.format(
        total_events=total_events,
        appearances=total_appearances,
        disappearances=total_disappearances,
        generation_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        month_sections=month_sections
    )
    
    with open(filename, 'w', encoding='utf-8') as htmlfile:
        htmlfile.write(final_html)
    
    print(f"HTML report saved to {filename}")

def main():
    print("🕉️ ISKCON Maharaj Days Processor")
    print("=" * 50)
    print("Processing swamisiskcon.csv...")
    
    # Process the data
    maharaj_data = process_maharaj_data()
    
    # Generate summary
    generate_summary(maharaj_data)
    
    # Save to JSON
    save_to_json(maharaj_data)
    
    # Generate HTML report
    generate_html_report(maharaj_data)
    
    print("\n✅ Processing completed successfully!")
    print("\nGenerated files:")
    print("- iskcon_maharaj_days.json (JSON format)")
    print("- iskcon_maharaj_days.html (HTML report)")

if __name__ == "__main__":
    main()