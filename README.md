# Auto Job Applier

## Setup
1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    python -m nltk.downloader stopwords
    ```
2.  **Environment Variables**:
    Create a `.env` file in the root directory:
    ```
    JOBDATA_API_KEY=your_api_key_here
    RESUME_PATH=my_resume.pdf
    ```
3.  **Resume**:
    Place your resume PDF (or clear text file) in the project root and ensure `RESUME_PATH` matches its name.

## Running
Run the main script:
```bash
python main.py
```

## How it works
1.  **Search**: Fetches jobs from JobData API based on your query.
2.  **Evaluate**: Extracts text from your resume and the job description, compares them using TF-IDF.
3.  **Track**: Logs every job and its score to `data/jobs.db`.
