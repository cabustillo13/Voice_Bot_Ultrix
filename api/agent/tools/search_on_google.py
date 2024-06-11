import requests
import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()


def google_search(query):
    """Search on Google"""
    params = {
        'api_key': os.getenv("SERPAPI_API"),
        'q': query,
        'engine': 'google',
        #"location": "Austin, Texas, United States",
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        'no_cache': 'true'
    }

    response = requests.get('https://serpapi.com/search.json', params=params)
    results = response.json()

    # Check the results and Filter by relevant fields
    if len(results["organic_results"]) == 0:
        answer = {
            "peopleAlsoAsk": [],
            "relatedSearches": [],
            "organicResults": [] 
        }
    else:
        # Cleaning irrelevant fields
        try:
            related_questions_cleaned = [
                {
                    'question': item.get('question', ''),
                    'snippet': item.get('snippet', ''),
                    'title': item.get('title', ''),
                    'link': item.get('link', '')
                }
                for item in results["related_questions"]
            ]
        except:
            related_questions_cleaned = []

        try:
            related_searches_cleaned = [
                {
                    'query': item.get('query', ''),
                }
                for item in results["related_searches"]
            ]
        except:
            related_searches_cleaned = []

        try:
            organic_results_cleaned = [
                {
                    'title': item.get('title', ''),
                    'link': item.get('link', ''),
                    'snippet': item.get('snippet', ''),
                    'sitelinks': item.get('sitelinks', {}),
                    'position': item.get('position', ''),
                }
                for item in results["organic_results"]
            ]
        except:
            organic_results_cleaned = []
        
        raw_answer = {
            "peopleAlsoAsk": related_questions_cleaned,
            "relatedSearches": related_searches_cleaned,
            "organicResults": organic_results_cleaned, 
        }

        # Make a friendly summary
        answer = str(raw_answer)

    return answer
