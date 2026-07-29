import os

from dotenv import load_dotenv
from google import genai
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests


load_dotenv()

MODEL_NAME = "gemini-3.5-flash-lite"


SOURCE_WEIGHTS = {
    "Reuters": 1.0,
    "Bloomberg": 1.0,
    "CNBC": 0.9,
    "Yahoo Finance": 0.8,
    "Business Insider": 0.7,
    "Investor's Business Daily": 0.7,
    "The Motley Fool": 0.6,
}


client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)


session = requests.Session()

retry = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[
        429,
        500,
        502,
        503,
        504,
    ],
)

session.mount(
    "https://",
    HTTPAdapter(max_retries=retry),
)