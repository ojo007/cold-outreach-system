# AI-Powered Cold Outreach System

This system automates the process of generating personalized cold outreach emails for the German real estate market. It handles lead scraping, email personalization using LLMs, and sending test emails.

## Project Overview

The system follows a simple pipeline:

1. **Lead Scraping**: Find potential leads from public sources
2. **Email Generation**: Create personalized emails in German using LLMs
3. **Email Sending**: Send test emails (configurable for actual sending)
4. **Cost Estimation**: Calculate costs for scaling the system

## Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository or extract the files to your desired location

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up configuration files:
   - Copy the example config files from `examples/` to `config/`
   - Edit the configuration files with your API keys and settings

### Configuration

The system uses three main configuration files:

1. **settings.json**: General settings for the system
2. **api_credentials.json**: API keys for LLMs and other services
3. **email_settings.json**: Email server settings and credentials

## Usage

### Running the System

Run the complete pipeline with:
```
python main.py
```

### Command Line Options

- `--skip-scraping`: Skip lead scraping and use existing leads
- `--skip-sending`: Skip sending the test email
- `--num-leads NUMBER`: Specify the number of leads to scrape (default: 20)
- `--scale-to NUMBER`: Specify number of emails per day for cost estimate (default: 100)

Example:
```
python main.py --num-leads 10 --skip-sending
```

## Project Structure

```
cold-outreach-system/
│
├── config/                 # Configuration files
│   ├── settings.json       # General settings
│   ├── api_credentials.json # API keys
│   └── email_settings.json # Email server settings
│
├── scripts/                # Core functionality
│   ├── lead_scraper.py     # Lead generation script
│   ├── email_generator.py  # Email creation using LLMs
│   ├── email_sender.py     # Email delivery script
│   └── utils.py            # Utility functions
│
├── data/                   # Data storage
│   ├── leads.csv           # Scraped leads
│   ├── personalized_emails.csv # Generated emails
│   └── sent_emails.csv     # Email sending logs
│
├── templates/              # Email templates
│   ├── email_template.txt  # Base email template
│   └── email_subjects.txt  # Subject line options
│
├── main.py                 # Main script to run pipeline
│
└── README.md               # Documentation
```

## Cost Overview

The system calculates estimated costs for scaling to your specified number of emails per day. This includes:

- LLM API costs for email generation
- Email service costs
- Hosting and infrastructure costs

The estimate is saved to `data/cost_estimates.json`.

## Personalization Approach

This system uses LLMs to create highly personalized emails by:

1. Extracting relevant information from lead data
2. Using templates as a foundation
3. Leveraging LLMs to craft natural-sounding, personalized content
4. Incorporating company and location-specific details

Personalization significantly improves conversion rates compared to generic mass emails.

## Maintenance & Extension

The system is designed to be easy to maintain and extend:

- Modular structure with separate scripts for each function
- Well-documented code with clear comments
- Simple file-based storage that requires no database setup
- Configuration via JSON files instead of hardcoded values

To extend the system, you can:
- Add new lead sources in `lead_scraper.py`
- Create additional email templates in the `templates` directory
- Implement more sophisticated personalization in `email_generator.py`
- Add follow-up capabilities to `email_sender.py`

## Troubleshooting

Common issues:
- **API Key Errors**: Check your credentials in `config/api_credentials.json`
- **Email Sending Failures**: Verify settings in `config/email_settings.json`
- **Missing Files**: Ensure all required directories and files exist
