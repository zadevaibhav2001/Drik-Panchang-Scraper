const fetch = require('node-fetch');
const { JSDOM } = require('jsdom');

exports.handler = async (event, context) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  try {
    const year = event.queryStringParameters?.year || '2025';
    const url = `https://www.drikpanchang.com/iskcon/iskcon-event-calendar.html?year=${year}`;
    
    const response = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    });
    
    const html = await response.text();
    const dom = new JSDOM(html);
    const document = dom.window.document;
    
    const eventInfos = document.querySelectorAll('.dpEventInfo');
    const events = [];
    
    eventInfos.forEach(eventInfo => {
      const gregDate = eventInfo.querySelector('.dpEventGregDate');
      const eventName = eventInfo.querySelector('.dpEventName.dpHinduEventColor');
      
      if (gregDate && eventName) {
        events.push({
          date: gregDate.textContent.trim(),
          name: eventName.textContent.trim()
        });
      }
    });
    
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({ success: true, events })
    };
  } catch (error) {
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ success: false, error: error.message })
    };
  }
};