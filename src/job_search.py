import requests
from src.config import Config

class JobSearch:
    BASE_URL = "https://jobdataapi.com/api/jobs/"

    def __init__(self):
        self.api_key = Config.JOBDATA_API_KEY
    
    def fetch_jobs(self, query="software engineer", country="us", days_ago=1):
        """
        Fetches jobs from the API.
        """
        if Config.MOCK_MODE:
            print(" [DEBUG] MOCK_MODE is ON. Returning dummy job data.")
            from src.mock_data import MOCK_JOBS
            return MOCK_JOBS

        # Calculate date for filtering (jobs posted in last N days)
        from datetime import datetime, timedelta
        posted_after_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')

        headers = {
            "Authorization": f"Api-Key {self.api_key}",
            "User-Agent": "AutoJobApplier/1.0"
        }
        params = {
            "text": query,
            "country": country,
            "posted_after": posted_after_date,
            "limit": 100  # Adjust as needed
        }
        
        try:
            print(f"Fetching jobs for '{query}' posted after {posted_after_date}...")
            response = requests.get(self.BASE_URL, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                # Assuming data structure is a list or dict with 'results'
                return data.get('results', []) if isinstance(data, dict) else data
            else:
                print(f"Error fetching jobs: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            print(f"Exception during job fetch: {e}")
            return []
