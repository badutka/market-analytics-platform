from google.cloud import bigquery
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp-key.json"

PROJECT_ID = "ms-fin-analytics-dev"


client = bigquery.Client(project=PROJECT_ID)


def store_dataframe(
    dataframe,
    table,
    write_disposition="WRITE_APPEND",
):

    job_config = bigquery.LoadJobConfig(write_disposition=write_disposition)

    job = client.load_table_from_dataframe(
        dataframe,
        table,
        job_config=job_config,
    )

    job.result()
