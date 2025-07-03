import streamlit as st
import os
from utils import load_excel
from database_handler import DatabaseHandler
from llm_handler import LLMHandler

st.set_page_config(page_title="NLP to SQL", layout="wide")
st.title("📈 Excel Insights With Simple Text")

uploaded_file = st.file_uploader("📤 Upload Excel/CSV File", type=["xlsx", "csv"])

if uploaded_file:
    df = load_excel(uploaded_file)

    if df is not None:
        file_base = os.path.splitext(uploaded_file.name)[0].replace(" ", "_").lower()
        db_name = f"{file_base}.db"
        table_name = file_base

        st.subheader(f"Top Records from `{table_name}`")
        st.dataframe(df.head(), use_container_width=True)

        db_handler = DatabaseHandler(db_name)
        db_handler.save_dataframe_to_db(df, table_name)

        st.success(f"Saved to `{db_name}` → Table: `{table_name}`")

        columns = db_handler.get_column_names(table_name)

        question = st.text_input("Ask a natural language question:")

        if question:
            llm = LLMHandler()
            try:
                sql_query = llm.get_sql_query(question, columns, table_name)
                st.code(sql_query, language="sql")
                results = db_handler.execute_query(sql_query)
                st.dataframe(results, use_container_width=True)
            except Exception as e:
                st.error(f"❌ {str(e)}")
