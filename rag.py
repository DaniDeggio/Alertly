from llama_index.core import (
    VectorStoreIndex
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.groq import Groq
# import os
# from dotenv import load_dotenv
# load_dotenv()
import warnings
warnings.filterwarnings('ignore')

from IPython.display import Markdown, display

from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    select,
)

engine = create_engine("sqlite:///:memory:")
metadata_obj = MetaData()

# create city SQL table
table_name = "city_stats"
city_stats_table = Table(
    table_name,
    metadata_obj,
    Column("city_name", String(16), primary_key=True),
    Column("population", Integer),
    Column("country", String(16), nullable=False),
)
metadata_obj.create_all(engine)

from llama_index.core import SQLDatabase
from google.colab import userdata
GROQ_API_KEY = userdata.get('groq')

sql_database = SQLDatabase(engine, include_tables=["city_stats"])

sql_database = SQLDatabase(engine, include_tables=["city_stats"])
from sqlalchemy import insert

rows = [
    {"city_name": "Toronto", "population": 2930000, "country": "Canada"},
    {"city_name": "Tokyo", "population": 13960000, "country": "Japan"},
    {
        "city_name": "Chicago",
        "population": 2679000,
        "country": "United States",
    },
    {"city_name": "Seoul", "population": 9776000, "country": "South Korea"},
]
for row in rows:
    stmt = insert(city_stats_table).values(**row)
    with engine.begin() as connection:
        cursor = connection.execute(stmt)

# view current table
stmt = select(
    city_stats_table.c.city_name,
    city_stats_table.c.population,
    city_stats_table.c.country,
).select_from(city_stats_table)

with engine.connect() as connection:
    results = connection.execute(stmt).fetchall()
    print(results)

from sqlalchemy import text

with engine.connect() as con:
    rows = con.execute(text("SELECT city_name from city_stats"))
    for row in rows:
        print(row)

llm = Groq(model="llama3-70b-8192", api_key=GROQ_API_KEY)

embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

from llama_index.core.query_engine import NLSQLTableQueryEngine

query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database, tables=["city_stats"], llm=llm, embed_model=embed_model
)
query_str = "Which city has the highest population?"
response = query_engine.query(query_str)

display(Markdown(f"<b>{response}</b>"))

from llama_index.core.retrievers import NLSQLRetriever

# default retrieval (return_raw=True)
nl_sql_retriever = NLSQLRetriever(
    sql_database, tables=["city_stats"], return_raw=True,
    llm=llm, embed_model=embed_model
)

results = nl_sql_retriever.retrieve(
    "Return the top 5 cities (along with their populations) with the highest population."
)

from llama_index.core.response.notebook_utils import display_source_node

for n in results:
    display_source_node(n)

# default retrieval (return_raw=False)
nl_sql_retriever = NLSQLRetriever(
    sql_database, tables=["city_stats"], return_raw=False, llm=llm, embed_model=embed_model
)

results = nl_sql_retriever.retrieve(
    "Return the top 5 cities (along with their populations) with the highest population."
)

# NOTE: all the content is in the metadata
for n in results:
    display_source_node(n, show_source_metadata=True)

from llama_index.core.query_engine import RetrieverQueryEngine

query_engine = RetrieverQueryEngine.from_args(nl_sql_retriever, llm=llm, embed_model=embed_model)

response = query_engine.query(
    "Return the top 5 cities (along with their populations) with the highest population."
)

print(str(response))

