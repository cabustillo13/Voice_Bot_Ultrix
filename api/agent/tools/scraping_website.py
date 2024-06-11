import requests
from bs4 import BeautifulSoup

from api.agent.tools.call_playfetch import call_llm


def summary_web_scraping(website_content):
    """Human Friendly output of Web Scraping"""
    # LLM
    url = "https://api.playfetch.ai/5726537974284288/summaryWebScraping"
    data = {
        "website_content": website_content
    }

    output = call_llm(url, data)

    return output


def get_text_from_website(url):
    """Get all text from a website"""
    try:
        # Send an HTTP request to the specified URL
        response = requests.get(url)
        response.raise_for_status()  # Check for any errors in the HTTP request

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract text from the parsed HTML
        text = soup.get_text(separator='\n', strip=True)

        # Make a friendly summary
        output = summary_web_scraping(str(text))

        return output

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return "Failed to retrieve text from the website."
