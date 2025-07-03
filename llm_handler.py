import os
from config import GEMINI_API_KEY
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class LLMHandler:
    def __init__(self):
        os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.1)

        self.prompt_template = PromptTemplate(
            input_variables=["question", "columns", "table_name"],
            template="""
You are an expert SQL assistant. Generate a valid SQL query for the given user question.

Table: {table_name}
Columns: {columns}

Instructions:
- Use only the above table and columns
- Wrap column names with spaces using double quotes (e.g., "Product line")
- Output ONLY the SQL query without explanations

User question:
{question}
"""
        )

        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

    def get_sql_query(self, question, columns, table_name):
        columns_str = ", ".join(columns)
        raw = self.chain.run(question=question, columns=columns_str, table_name=table_name)
        return raw.replace("```sql", "").replace("```", "").strip()
