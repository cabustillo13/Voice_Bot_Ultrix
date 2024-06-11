import requests
from bs4 import BeautifulSoup


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

        return text

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return "Failed to retrieve text from the website."
