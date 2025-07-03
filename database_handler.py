import pandas as pd
from sqlalchemy import create_engine, inspect, text

class DatabaseHandler:
    def __init__(self, db_name):
        """
        Initializes a connection to the SQLite database using SQLAlchemy.

        Parameters:
        db_name (str): Name of the database file to connect to or create.
        """
        self.engine = create_engine(f"sqlite:///{db_name}")
        self.connection = self.engine.connect()

    def save_dataframe_to_db(self, df, table_name):
        """
        Cleans column names and saves the DataFrame to a table in the database.

        Parameters:
        df (pd.DataFrame): The DataFrame to store.
        table_name (str): Name of the table to create or overwrite in the database.
        """
        df.columns = df.columns.str.strip().str.replace('"', '').str.replace("'", "")
        df.to_sql(table_name, self.engine, if_exists='replace', index=False)

    def get_column_names(self, table_name):
        """
        Fetches the column names of the given table from the database.

        Parameters:
        table_name (str): Name of the table to inspect.

        Returns:
        list: A list of column names.
        """
        inspector = inspect(self.engine)
        return [col["name"] for col in inspector.get_columns(table_name)]

    def execute_query(self, query):
        """
        Executes an SQL query and returns the result as a DataFrame.

        Parameters:
        query (str): The SQL query to execute.

        Returns:
        pd.DataFrame: Resulting data from the query.

        Raises:
        Exception: If the SQL query fails.
        """
        try:
            return pd.read_sql_query(text(query), self.connection)
        except Exception as e:
            raise Exception(f"Query Error: {str(e)}")

