import pandas as pd
from sqlalchemy import create_engine, inspect, text

class DatabaseHandler:
    def __init__(self, db_name):
        self.engine = create_engine(f"sqlite:///{db_name}")
        self.connection = self.engine.connect()

    def save_dataframe_to_db(self, df, table_name):
        df.columns = df.columns.str.strip().str.replace('"', '').str.replace("'", "")
        df.to_sql(table_name, self.engine, if_exists='replace', index=False)

    def get_column_names(self, table_name):
        inspector = inspect(self.engine)
        return [col["name"] for col in inspector.get_columns(table_name)]

    def execute_query(self, query):
        try:
            return pd.read_sql_query(text(query), self.connection)
        except Exception as e:
            raise Exception(f"Query Error: {str(e)}")
