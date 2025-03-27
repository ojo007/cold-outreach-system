#!/usr/bin/env python3
"""
AI-Powered Cold Outreach System
Main script that runs the complete pipeline
"""

import os
import sys
import json
import argparse
from pathlib import Path
import datetime

# Import components from scripts
from scripts.lead_scraper import scrape_leads
from scripts.email_generator import generate_emails
from scripts.email_sender import send_emails
from scripts.utils import calculate_cost_estimate, save_json_file, ensure_data_directory


def setup_directories():
    """Create necessary directories if they don't exist"""
    Path("data").mkdir(exist_ok=True)
    Path("config").mkdir(exist_ok=True)
    Path("templates").mkdir(exist_ok=True)

    # Check for required files
    required_files = [
        "config/settings.json",
        "config/api_credentials.json",
        "config/email_settings.json",
        "templates/email_template.txt"
    ]

    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print("Error: The following required files are missing:")
        for file in missing_files:
            print(f"  - {file}")
        print("\nPlease create these files before running the system.")
        sys.exit(1)


def run_pipeline(args):
    """Run the complete outreach pipeline"""
    start_time = datetime.datetime.now()
    print(f"Starting cold outreach pipeline at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Step 1: Scrape leads (if not skipped)
    leads = None
    if not args.skip_scraping:
        print("\n===== STEP 1: SCRAPING LEADS =====")
        leads = scrape_leads(args.num_leads)

    # Step 2: Generate personalized emails
    print("\n===== STEP 2: GENERATING EMAILS =====")
    emails_data = generate_emails(leads)

    # Step 3: Send test email (if not skipped)
    if not args.skip_sending:
        print("\n===== STEP 3: SENDING TEST EMAIL =====")
        send_emails(emails_data)

    # Step 4: Generate cost estimate
    print("\n===== STEP 4: GENERATING COST ESTIMATE =====")
    cost_data = calculate_cost_estimate(args.scale_to)
    data_dir = ensure_data_directory()
    save_json_file(cost_data, data_dir / "cost_estimates.json")

    print(f"\nCost estimate for scaling to {args.scale_to} emails per day:")
    print(f"  - Monthly emails: {cost_data['emails_per_month']}")
    print(f"  - Estimated token usage: {cost_data['estimated_token_usage']:,}")
    print(f"  - LLM cost: €{cost_data['estimated_monthly_llm_cost']:.2f}")
    print(f"  - Other costs: €{sum(cost_data['other_costs'].values()):.2f}")
    print(f"  - Total monthly cost: €{cost_data['total_estimated_monthly_cost']:.2f}")
    print(f"  - Cost per email: €{cost_data['total_estimated_monthly_cost'] / cost_data['emails_per_month']:.4f}")

    # Completion summary
    end_time = datetime.datetime.now()
    duration = (end_time - start_time).total_seconds()

    print("\n===== PIPELINE COMPLETED =====")
    print(f"Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Ended: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duration: {duration:.2f} seconds")
    print(f"\nResults:")
    print(f"  - Leads scraped: {len(emails_data) if emails_data else 0}")
    print(f"  - Emails generated: {len(emails_data) if emails_data else 0}")
    print(f"  - Test email sent: {'Yes' if not args.skip_sending else 'No'}")
    print(f"  - Cost estimate generated: Yes")
    print(f"\nAll data saved in the 'data' directory")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='AI-Powered Cold Outreach System')
    parser.add_argument('--skip-scraping', action='store_true', help='Skip lead scraping and use existing leads.csv')
    parser.add_argument('--skip-sending', action='store_true', help='Skip sending test email')
    parser.add_argument('--num-leads', type=int, default=20, help='Number of leads to scrape')
    parser.add_argument('--scale-to', type=int, default=100, help='Number of emails per day for cost estimate')
    args = parser.parse_args()

    # Ensure all necessary directories and files exist
    setup_directories()

    # Run the pipeline
    run_pipeline(args)


if __name__ == "__main__":
    main()