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

Inkle/
├── main.py # Main Python entry point
├── app.py # Application setup 
├── requirements.txt # Python dependencies
├── .env.example # Configuration template
├── dashboard_connected.html # Main dashboard frontend (rename to index.html for deployment)
├── README.md # Project documentation
├── SETUP_GUIDE.md # quick setup
│
└── src/
├── init.py
├── services/
│ ├── init.py
│ ├── geocoding.py # Nominatim API service
│ ├── weather.py # Open-Meteo API service
│ └── tourism.py # Overpass API service
│
└── agents/
├── init.py
├── tools.py # LangChain tool wrappers
└── orchestrator.py # Parent agent

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


