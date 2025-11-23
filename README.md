# INKLE

## Tourist Buddy

A modern travel dashboard for exploring weather and curated tourist attractions across India.  
This project demonstrates a multi-agent architecture for destination-based recommendations using real (or demo) data in a clean, interactive web dashboard.

---

##  Demo

Deployed via [Netlify](https://www.netlify.com/).

**[Live site here](https://inkle-assessment.netlify.app/)**

---

## Project Structure/ Core Project Files

1. Understand Your Current Structure (as shown)
text
Inkle/
├── main.py
├── app.py
├── requirements.txt
├── .env.example
├── dashboard_connected.html
├── README.md
├── SETUP_GUIDE.md
│
└── src/
    ├── __init__.py
    ├── services/
    │   ├── __init__.py
    │   ├── geocoding.py
    │   ├── weather.py
    │   └── tourism.py
    │
    └── agents/
        ├── __init__.py
        ├── tools.py
        └── orchestrator.py
        
2. Common Modifications
   Rename files (e.g. for Netlify deployment):
Rename dashboard_connected.html to index.html.

---

## How It Works

USER question  
↓  
PARENT AGENT (Orchestrator)  
├─→ Weather Agent   (find temperature)  
└─→ Service Agent   (find locations)  
↓                     ↓  
PARENT AGENT merges both results  
↓  
RESPONSE:  
"In Bangalore, the current temperature is 24°C.  
Here are 5 places to visit: Lalbagh, Cubbon Park, Bangalore Palace, ISKCON Temple, Vidhana Soudha."


