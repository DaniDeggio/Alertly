'use client'

import { useState } from 'react'
import Layout from '../components/layout'

export default function ReportPage() {
  const [report, setReport] = useState('')
  const [tematica, setTematica] = useState('')
  const [coordinate, setCoordinate] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    // Verifica che il contenuto e la tematica siano presenti
    if (!report || !tematica) {
      setError('Please fill in all required fields.')
      setSuccess(false)
      return
    }

    setLoading(true)
    setError('')
    setSuccess(false)

    try {
      const response = await fetch('http://localhost:5000/segnalazione', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          contenuto: report,
          tematica: tematica,
          coordinate: coordinate || '',  // Può essere opzionale
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to submit report')
      }

      // Successo: Reset dei campi e messaggio di conferma
      setReport('')
      setTematica('')
      setCoordinate('')
      setSuccess(true)
    } catch (err) {
      console.error('Error submitting report:', err)
      setError('There was an error submitting your report.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Layout>
      <div className="max-w-2xl mx-auto">
        <h2 className="text-3xl font-bold mb-6 text-gray-900">Submit a Report</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <textarea
            value={report}
            onChange={(e) => setReport(e.target.value)}
            placeholder="Describe the issue you've noticed..."
            className="w-full h-40 p-4 text-gray-800 bg-gray-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 border border-gray-300"
            required
          />
          
          <input
            type="text"
            value={tematica}
            onChange={(e) => setTematica(e.target.value)}
            placeholder="Enter the issue category (e.g., Rifiuti, Traffico, etc.)"
            className="w-full p-4 text-gray-800 bg-gray-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 border border-gray-300"
            required
          />

          <input
            type="text"
            value={coordinate}
            onChange={(e) => setCoordinate(e.target.value)}
            placeholder="Enter coordinates (optional)"
            className="w-full p-4 text-gray-800 bg-gray-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 border border-gray-300"
          />

          {error && <p className="text-red-500">{error}</p>}
          {success && <p className="text-green-500">Your report has been successfully submitted!</p>}

          {/* Sostituito il componente Button con un normale bottone HTML */}
          <button type="submit" 
                  className="w-full py-2 px-4 bg-blue-500 text-white font-semibold rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  disabled={loading}>
            {loading ? 'Submitting...' : 'Submit Report'}
          </button>
        </form>
      </div>
    </Layout>
  )
}
