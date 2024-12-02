import os
import sqlite3
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from toolhouse import Toolhouse
from llama_index.core import SQLDatabase
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.query_engine import NLSQLTableQueryEngine
from sqlalchemy import create_engine
from llama_index.llms.groq import Groq
from flask_cors import CORS

# Carica le variabili di ambiente dal file .env
load_dotenv()


# Configurazione del database
DATABASE = 'segnalazioni.db'

# Setup di Flask per il backend
app = Flask(__name__)
CORS(app)

# Setup dei client per Groq e Toolhouse
client = Groq(model="llama-3.1-70b-versatile", api_key=os.environ.get('GROQ_API_KEY'))
th = Toolhouse()

# Modello Llama 3.1 fine-tuned per l'uso con Toolhouse
MODEL = "llama3-groq-70b-8192-tool-use-preview"

# Funzione per connettersi al database SQLite usando SQLAlchemy
def connect_sqlalchemy_db():
    engine = create_engine(f"sqlite:///{DATABASE}")
    return engine

# Funzione per configurare LLM e embedder
def configure_llm_and_embeddings():
    # Configura il modello LLM Groq e il modello di embedding da Hugging Face
    llm = Groq(model="llama-3.1-70b-versatile", api_key=os.environ.get('GROQ_API_KEY'))
    embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return llm, embed_model

# Funzione per configurare il motore di query NLSQL
def configure_query_engine():
    engine = connect_sqlalchemy_db()
    sql_database = SQLDatabase(engine, include_tables=["segnalazioni"])  # Usa la tabella esistente
    llm, embed_model = configure_llm_and_embeddings()
    query_engine = NLSQLTableQueryEngine(sql_database=sql_database, tables=["segnalazioni"], llm=llm, embed_model=embed_model)
    return query_engine

# Funzione per eseguire una query in linguaggio naturale con il motore di query configurato
def run_nlsql_query(query_str):
    query_engine = configure_query_engine()
    response = query_engine.query(query_str)
    return response

# Funzione per connettersi al database SQLite usando sqlite3 (solo per operazioni SQL dirette)
def connect_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Creazione della tabella delle segnalazioni (se non esiste già)
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS segnalazioni (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        coordinate TEXT,
        tematica TEXT NOT NULL,
        contenuto TEXT NOT NULL
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()

# Funzione per inserire una nuova segnalazione
def inserisci_segnalazione(coordinate, tematica, contenuto):
    conn = connect_db()
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO segnalazioni (coordinate, tematica, contenuto)
    VALUES (?, ?, ?)
    """
    cursor.execute(insert_query, (coordinate, tematica, contenuto))
    conn.commit()
    conn.close()
# Endpoint per aggiungere una segnalazione
@app.route('/segnalazione', methods=['POST'])
def add_segnalazione():
    data = request.json
    tematica = data.get('tematica')
    contenuto = data.get('contenuto')
    coordinate = data.get('coordinate')  # Campo opzionale

    if not tematica or not contenuto:
        return jsonify({"error": "Tematica e contenuto sono obbligatori"}), 400

    # Inserisci la segnalazione nel database
    inserisci_segnalazione(coordinate, tematica, contenuto)
    return jsonify({"message": "Segnalazione aggiunta con successo"}), 201

# Endpoint per recuperare tutte le segnalazioni
@app.route('/segnalazioni', methods=['GET'])
def get_segnalazioni():
    conn = connect_db()
    cursor = conn.cursor()
    select_query = "SELECT * FROM segnalazioni"
    cursor.execute(select_query)
    rows = cursor.fetchall()
    conn.close()

    segnalazioni = [dict(row) for row in rows]  # Converti in formato JSON
    return jsonify(segnalazioni)

# Endpoint per fare domande al sistema tramite NLSQL
@app.route('/pa/query', methods=['POST'])
def pa_query():
    data = request.json
    domanda = data.get('domanda')

    if not domanda:
        return jsonify({"error": "Domanda mancante"}), 400

    # Esegui la query NLSQL con Llama Index
    response = run_nlsql_query(domanda)

    # Risposta finale
    return jsonify({"response": str(response)})

# Funzione per avviare il server Flask
if __name__ == '__main__':
    # Crea la tabella delle segnalazioni all'avvio (se non esiste già)
    create_table()

    # Avvia il server Flask
    app.run(debug=True, host='0.0.0.0', port=5000)
