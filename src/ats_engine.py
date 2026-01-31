import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
import logging

# Ensure stopwords are downloaded
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class ATSEngine:
    def __init__(self, resume_text):
        self.resume_text = self.clean_text(resume_text)
        self.vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'))

    def clean_text(self, text):
        # Basic cleaning: remove special chars, lowercase
        text = re.sub(r'\W+', ' ', text)
        return text.lower().strip()

    def evaluate(self, job_description):
        """
        Returns a score between 0 and 100 based on cosine similarity.
        """
        clean_job = self.clean_text(job_description)
        
        # Vectorize
        vectors = self.vectorizer.fit_transform([self.resume_text, clean_job])
        
        # Calculate Cosine Similarity
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])
        score = similarity[0][0] * 100
        return round(score, 2)
