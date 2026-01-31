import sys
import os
from src.config import Config
from src.ats_engine import ATSEngine
from src.job_search import JobSearch
from src.tracker import JobTracker
from src.logger import setup_logging
import logging

def load_resume_text(path):
    if not os.path.exists(path):
        logging.error(f"Resume file not found at: {path}")
        return None
    
    if path.endswith('.pdf'):
        from pdfminer.high_level import extract_text
        return extract_text(path)
    else:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

def main():
    setup_logging()
    logging.info("Starting Auto Job Applier...")
    
    # 1. Load Resume
    resume_text = load_resume_text(Config.RESUME_PATH)
    if not resume_text:
        logging.critical("Please ensure your resume is at the path specified in Config (resume.pdf).")
        return

    # 2. Initialize Modules
    ats = ATSEngine(resume_text)
    searcher = JobSearch()
    tracker = JobTracker()
    
    # 3. Fetch Jobs
    jobs = searcher.fetch_jobs(query="machine learning AI engineer", days_ago=1)
    logging.info(f"Found {len(jobs)} jobs from the last day.")

    # Filter for ML/AI specific roles
    ml_keywords = ['machine learning', 'ml', 'ai', 'artificial intelligence', 'data scientist', 'deep learning']
    
    # 4. Process Jobs
    processed_count = 0
    for job in jobs:
        # Normalize fields (adjust based on actual API response)
        title = job.get('title', 'Unknown Title')
        company = job.get('company', {}).get('name', 'Unknown Company')
        description = job.get('description', '')
        url = job.get('url', '') # or 'apply_url'

        if not description:
            continue

        # Filter by job title containing ML/AI keywords
        if not any(keyword in title.lower() for keyword in ml_keywords):
            logging.debug(f"Skipping non-ML/AI job: {title}")
            continue

        if tracker.job_exists(url):
            logging.info(f"Skipping already processed job: {title}")
            continue

        # 5. Evaluate
        score = ats.evaluate(description)
        logging.info(f"Evaluated '{title}' at {company}: Score {score}")

        if score >= Config.MIN_ATS_SCORE:
            logging.info(f"  [TARGET ACQUIRED] Score {score} >= {Config.MIN_ATS_SCORE}")
            # Future: bot.apply(url)
            status = "Ready to Apply"
        else:
            status = "Skipped (Low Score)"
        
        tracker.log_job(company, title, url, description, score, status)
        processed_count += 1

    logging.info(f"Job processing complete. Processed {processed_count} ML/AI jobs.")

if __name__ == "__main__":
    main()
