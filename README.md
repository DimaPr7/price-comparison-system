# Price Comparison System

A full-stack web application for tracking and comparing product prices across multiple online stores with automated price scraping and historical analytics.

This project was developed as a **Bachelor’s thesis by Dmytro (2026)** in software engineering.

---

## 🌐 Live Demo

👉 [https://pricechecker-dmytro.org](https://pricechecker-dmytro.org)

---

## Project Goal

The goal of this system is to help users:
- Compare product prices across multiple online stores  
- Track price changes over time  
- Analyze price history trends  
- Save favorite products  

---

## Features

- 🔎 Product comparison across multiple stores  
- 📈 Price history tracking with charts (Chart.js)  
- ⭐ Favorites system  
- 👤 User authentication (register/login/profile)  
- 🏪 Multi-store product aggregation  
- 🕒 Automated price scraping (cron-based)  
- 📊 Historical price analytics  
- 📱 Responsive UI  

---

## Tech Stack

### Backend
- Python 3.11
- Django 5
- Django ORM
- PostgreSQL (production)
- SQLite (development)

### Frontend
- HTML / CSS
- JavaScript
- Chart.js

### Web Scraping
- Playwright
- BeautifulSoup4

### Deployment
- Render (Web Service + Cron Jobs)
- WhiteNoise (static files)

---

## System Architecture

- Django web application (UI + business logic)
- PostgreSQL database
- Playwright scraping engine
- Scheduled cron job for updates
- External e-commerce websites as data sources

---

## Price Scraping

Run manually:

```bash
python manage.py parse_prices
```

### Steps:
1. Load offers from DB
2. Open product pages via Playwright
3. Extract HTML
4. Parse prices with store-specific parsers
5. Save to `PriceHistory`
6. Skip unchanged values

---

## Run Locally

```bash
# Clone the repository
git clone https://github.com/yourusername/price-comparison-system.git
cd price-comparison-system

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations and start server
python manage.py migrate
python manage.py runserver
```

---

## Environment Variables

Create a `.env` file in the root directory and configure the following variables:

```ini
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
SECRET_KEY=
DEBUG=False
```

---

## Manual Parser Run

```bash
python manage.py parse_prices
```
*Fetches offers, parses prices, and saves history.*

---

## Key Challenges

- Playwright dynamic content scraping
- Cloudflare / anti-bot pages
- Multi-store parsing logic
- Price history optimization
- Render deployment + cron jobs

---


## Academic Context

Bachelor’s thesis project demonstrating:
- Full-stack development
- Web scraping
- Database design
- Cloud deployment
- Real-world data processing

---

## Author

**Dmytro Prokhach**  
*Bachelor’s Thesis Project — 2026*
