import os
import sqlite3
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from toolhouse import Toolhouse
from groq import Groq

# Carica le variabili di ambiente dal file .env
load_dotenv()

# Configurazione del database
DATABASE = 'segnalazioni.db'

# Setup di Flask per il backend
app = Flask(__name__)

# Setup dei client per Groq e Toolhouse
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
th = Toolhouse()

# Modello Llama 3.1 fine-tuned per l'uso con Toolhouse
MODEL = "llama3-groq-70b-8192-tool-use-preview"

# Funzione per connettersi al database SQLite
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
    
    # Salva i cambiamenti e chiudi la connessione
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

# Endpoint per la pubblica amministrazione che fa domande tramite Llama 3.1
@app.route('/pa/query', methods=['POST'])
def pa_query():
    data = request.json
    domanda = data.get('domanda')

    if not domanda:
        return jsonify({"error": "Domanda mancante"}), 400

    # Recupera gli strumenti da Toolhouse
    tools = th.get_tools()

    # Configura il messaggio per il modello Llama
    messages = [
        {"role": "user", "content": domanda}
    ]

    # Prima richiesta a Llama 3.1
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
    )

    # Esegui gli strumenti configurati 
    tool_run = th.run_tools(response)

    # Estendi il contesto con i risultati degli strumenti
    messages.extend(tool_run)

    # Risposta finale con il contesto aggiornato
    final_response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
    )

    return jsonify({"response": final_response.choices[0].message.content})

# Funzione per avviare il server Flask
if __name__ == '__main__':
    # Crea la tabella delle segnalazioni all'avvio
    create_table()
    
    # Avvia il server Flask
    app.run(debug=True, host='0.0.0.0', port=5000)
