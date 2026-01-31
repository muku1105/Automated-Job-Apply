import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    JOBDATA_API_KEY = os.getenv("JOBDATA_API_KEY", "")
    DB_PATH = os.path.join(os.getcwd(), "data", "jobs.db")
    MIN_ATS_SCORE = 85.0
    RESUME_PATH = os.getenv("RESUME_PATH", "resume.txt")
    
    # Mock Mode for testing without API Key
    MOCK_MODE = False

    # Bot settings
    HEADLESS = False  # Set to True for production
