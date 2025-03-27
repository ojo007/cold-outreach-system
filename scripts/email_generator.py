import json
import csv
import os
import requests
from pathlib import Path
from scripts.utils import load_api_credentials_secure, ensure_data_directory, save_csv_file


def load_config():
    """Load configuration settings"""
    with open('config/settings.json', 'r') as f:
        return json.load(f)


def load_template():
    """Load email template"""
    with open('templates/email_template.txt', 'r', encoding='utf-8') as f:
        return f.read()


def generate_personalized_email(lead, template):
    """
    Generate personalized email using LLM via direct API call
    Returns the personalized email text
    """
    credentials = load_api_credentials_secure()
    api_key = credentials["openai_api_key"]

    # Example LLM prompt
    prompt = f"""
    Create a personalized cold outreach email in German for a property management software.

    Company: {lead['company_name']}
    Contact: {lead['contact_name']}
    Position: {lead['position']}
    City: {lead['city']}
    Properties: {lead['properties_count']}

    The email should:
    1. Address them by name
    2. Reference their specific property management needs
    3. Mention how our software can help their specific business
    4. Include a clear call to action

    Keep it professional but conversational. Maximum 150 words.
    """

    try:
        # Direct API call without using the client
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": "gpt-3.5-turbo",  # Using gpt-3.5-turbo which is widely available
            "messages": [
                {"role": "system", "content": "You are an expert in creating personalized business emails in German."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            response_json = response.json()
            personalized_email = response_json["choices"][0]["message"]["content"].strip()
            return personalized_email
        else:
            print(f"API error: {response.status_code}, {response.text}")
            raise Exception(f"API returned status code {response.status_code}")

    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        # Fallback to template if API call fails
        return template.format(
            contact_name=lead['contact_name'],
            position=lead['position'],
            company_name=lead['company_name'],
            city=lead['city'],
            properties_count=lead['properties_count']
        )


def generate_emails(leads=None):
    """
    Generate personalized emails for each lead
    Returns a list of dictionaries with lead info and personalized emails
    """
    if leads is None:
        # Load leads from CSV if not provided
        leads = []
        try:
            with open('data/leads.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    leads.append(row)
        except FileNotFoundError:
            print("Error: leads.csv not found. Please run lead scraper first or provide leads.")
            return []

    template = load_template()
    results = []

    print(f"Generating personalized emails for {len(leads)} leads...")

    for i, lead in enumerate(leads):
        print(f"Processing lead {i + 1}/{len(leads)}: {lead['company_name']}")
        personalized_email = generate_personalized_email(lead, template)
        results.append({
            **lead,
            "personalized_email": personalized_email
        })

    # Save results to CSV
    ensure_data_directory()
    save_csv_file(results, 'data/personalized_emails.csv')

    print(f"Successfully generated {len(results)} personalized emails")
    return results


if __name__ == "__main__":
    generate_emails()