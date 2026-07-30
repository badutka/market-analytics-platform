from google.cloud import bigquery


class BigQueryClient:

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.client = bigquery.Client(project=project_id)

    def _table_ref(self, table: str):
        # When the table_id does not include a project ID, default_project is used.
        return bigquery.TableReference.from_string(
            table,
            default_project=self.project_id,
        )

    def write_dataframe(
        self,
        dataframe,
        table,
        write_disposition="WRITE_APPEND",
    ):
        table_ref = self._table_ref(table)

        job_config = bigquery.LoadJobConfig(write_disposition=write_disposition)

        job = self.client.load_table_from_dataframe(
            dataframe,
            table_ref,
            job_config=job_config,
        )

        job.result()

    def query_dataframe(self, query: str):
        return self.client.query(query).to_dataframe()

    def query_table_dataframe(self, table: str):
        table_ref = self._table_ref(table)

        query = f"""
            SELECT *
            FROM `{table_ref.project}.{table_ref.dataset_id}.{table_ref.table_id}`
        """

        return self.client.query(query).to_dataframe()