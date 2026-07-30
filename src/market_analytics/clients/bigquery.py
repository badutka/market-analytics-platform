from google.cloud import bigquery


class BigQueryClient:

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.client = bigquery.Client(project=project_id)

    def write_dataframe(
        self,
        dataframe,
        table,
        write_disposition="WRITE_APPEND",
    ):

        # When the table_id does not include a project ID, default_project is used.
        table_ref = bigquery.TableReference.from_string(table, default_project=self.project_id)

        job_config = bigquery.LoadJobConfig(write_disposition=write_disposition)

        job = self.client.load_table_from_dataframe(
            dataframe,
            table_ref,
            job_config=job_config,
        )

        job.result()
