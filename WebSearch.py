import os
from dotenv import load_dotenv
from toolhouse import Toolhouse
from groq import Groq

#load .env
load_dotenv()

# Crea il client per Groq e Toolhouse
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
th = Toolhouse()

# Modello fine-tuned per tool use
MODEL = "llama3-groq-70b-8192-tool-use-preview"

# Configura il messaggio dell'utente
messages = [
    {
        "role": "user",
        "content": "Find the top 5 companies in the field of AI and summarize their services."
    }
]

# Invio del messaggio all'LLM tramite Groq API
response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=th.get_tools(),
)

# Esegui gli strumenti configurati (in questo caso, la ricerca web)
tool_run = th.run_tools(response)

# Estendi il contesto con i risultati della ricerca
messages.extend(tool_run)

# Invia il contesto aggiornato per ottenere una risposta completa dall'LLM
final_response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=th.get_tools(),
)

# Stampa la risposta finale dell'LLM
print("LLM RESPONSE:", final_response.choices[0].message.content)
