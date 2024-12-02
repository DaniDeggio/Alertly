'use client'

import { useState } from 'react'
import Layout from '../components/layout'

export default function PublicAdministrationPage() {
  const [domanda, setDomanda] = useState('') // Per la domanda dell'utente
  const [response, setResponse] = useState('') // Per la risposta dal server
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    // Verifica che la domanda sia presente
    if (!domanda) {
      setError('Inserisci una domanda.')
      return
    }

    setLoading(true)
    setError('')
    setResponse('')
	try {
	const res = await fetch('http://localhost:5000/pa/query', {
		method: 'POST',
		headers: {
		'Content-Type': 'application/json',
		},
		body: JSON.stringify({
		domanda: domanda, // Invio della domanda all'endpoint
		}),
	});

	if (!res.ok) {
		throw new Error('Failed to submit the query');
	}

	const data = await res.json(); // Assumiamo che la risposta sia in formato JSON
	setResponse(data.response || 'Nessuna risposta trovata.'); // Modifica qui!
	} catch (err) {
	console.error('Error submitting the query:', err);
	setError('Si è verificato un errore durante l\'invio della domanda.');
	} finally {
	setLoading(false);
	}	
  }

  return (
    <Layout>
      <div className="max-w-2xl mx-auto">
        <h2 className="text-3xl font-bold mb-6 text-gray-900">Pubblica Amministrazione - Richieste</h2>

        {/* Form per inviare la domanda */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="flex items-center">
            <input
              type="text"
              value={domanda}
              onChange={(e) => setDomanda(e.target.value)}
              placeholder="Inserisci la tua domanda..."
              className="flex-1 p-4 text-gray-800 bg-gray-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 border border-gray-300"
              required
            />
            <button type="submit" 
                    className="ml-4 py-2 px-4 bg-blue-500 text-white font-semibold rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    disabled={loading}>
              {loading ? 'Inviando...' : 'Invia'}
            </button>
          </div>
        </form>

        {/* Messaggi di errore */}
        {error && <p className="text-red-500 mt-4">{error}</p>}

        {/* Box per mostrare la risposta dal server */}
        {response && (
          <div className="mt-8 p-4 bg-gray-100 rounded-lg border border-gray-300">
            <h3 className="text-xl font-bold mb-2">Risposta:</h3>
            <p className="text-gray-800">{response}</p>
          </div>
        )}
      </div>
    </Layout>
  )
}
