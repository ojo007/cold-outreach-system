import json
import csv
import random
import time
from pathlib import Path


def load_config():
    """Load configuration settings"""
    with open('config/settings.json', 'r') as f:
        return json.load(f)


def load_credentials():
    """Load API credentials"""
    with open('config/api_credentials.json', 'r') as f:
        return json.load(f)


def scrape_leads(num_leads=20):
    """
    Scrape leads from various sources
    Returns a list of lead data dictionaries
    """
    config = load_config()
    credentials = load_credentials()

    print(f"Starting to scrape {num_leads} leads for the {config['market']} market...")

    # This is where you'd implement actual scraping logic
    # For demonstration, we'll create sample data
    leads = []

    # Example property companies in Germany
    company_types = ["Immobilienmakler", "Hausverwaltung", "Immobilienberater", "Bauträger"]
    cities = ["Berlin", "München", "Hamburg", "Frankfurt", "Köln", "Düsseldorf", "Stuttgart"]

    for i in range(num_leads):
        lead = {
            "id": i + 1,
            "company_name": f"{random.choice(['ABC', 'XYZ', 'Best', 'Top', 'Prime'])} {random.choice(company_types)} {random.choice(cities)}",
            "contact_name": f"{random.choice(['Hans', 'Peter', 'Michael', 'Thomas', 'Andreas'])} {random.choice(['Müller', 'Schmidt', 'Weber', 'Schneider', 'Fischer'])}",
            "position": random.choice(["Geschäftsführer", "Inhaber", "Verkaufsleiter", "Makler"]),
            "email": f"contact{i + 1}@example-{i + 1}.de",
            "phone": f"+49 {random.randint(100, 999)} {random.randint(1000000, 9999999)}",
            "website": f"https://www.immobilien-{i + 1}.de",
            "city": random.choice(cities),
            "properties_count": random.randint(5, 100),
            "source": random.choice(config["lead_sources"])
        }
        leads.append(lead)

        # Simulate scraping delay
        time.sleep(0.1)

    # Save to CSV file
    Path("data").mkdir(exist_ok=True)
    with open('data/leads.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=leads[0].keys())
        writer.writeheader()
        writer.writerows(leads)

    print(f"Successfully scraped and saved {len(leads)} leads to data/leads.csv")
    return leads


if __name__ == "__main__":
    scrape_leads()