import json
import csv
import os
from pathlib import Path
from dotenv import load_dotenv


def ensure_data_directory():
    """Ensure data directory exists"""
    Path("data").mkdir(exist_ok=True)
    return Path("data")


def load_json_file(filepath):
    """Load and parse a JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json_file(data, filepath):
    """Save data to a JSON file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_csv_file(filepath):
    """Load data from a CSV file"""
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        pass
    return data


def save_csv_file(data, filepath, fieldnames=None):
    """Save data to a CSV file"""
    if not data:
        return

    if fieldnames is None:
        fieldnames = data[0].keys()

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def load_api_credentials_secure():
    """Load API credentials from environment variables first, then config file as fallback"""
    # Load environment variables from .env file if it exists
    load_dotenv()

    # Try to get API key from environment first
    openai_api_key = os.environ.get('OPENAI_API_KEY')

    # If not in environment, try config file
    if not openai_api_key:
        try:
            with open('config/api_credentials.json', 'r') as f:
                credentials = json.load(f)
                openai_api_key = credentials.get('llm_api', {}).get('api_key')
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            pass

    if not openai_api_key:
        print("Warning: No OpenAI API key found. Please set OPENAI_API_KEY environment variable.")

    return {
        "openai_api_key": openai_api_key
    }


def calculate_cost_estimate(num_emails, llm_cost_per_1k_tokens=0.03, avg_tokens_per_email=500):
    """Calculate estimated cost for generating emails"""
    token_cost = (num_emails * avg_tokens_per_email / 1000) * llm_cost_per_1k_tokens
    return {
        "emails_per_month": num_emails * 22,  # assuming 22 working days
        "estimated_token_usage": num_emails * avg_tokens_per_email * 22,
        "estimated_monthly_llm_cost": token_cost * 22,
        "other_costs": {
            "email_service": 10,  # example monthly cost
            "data_sources": 0,  # using free sources
            "hosting": 5  # minimal hosting
        },
        "total_estimated_monthly_cost": (token_cost * 22) + 15
    }