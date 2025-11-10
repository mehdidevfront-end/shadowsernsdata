import React, { useState } from 'react'

export default function ChatBox({ apiUrl = '/qa' }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  async function send() {
    if (!input) return
    const userMsg = { role: 'user', text: input }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setLoading(true)
    try {
      const res = await fetch(apiUrl, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ question: input }) })
      const j = await res.json()
      const botMsg = { role: 'bot', text: j.answer }
      setMessages(prev => [...prev, botMsg])
    } catch (e) {
      setMessages(prev => [...prev, { role: 'bot', text: 'Error: ' + (e.message || e) }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="border p-4 rounded">
      <div className="mb-2 h-64 overflow-auto bg-white p-2">
        {messages.map((m, i) => (
          <div key={i} className={m.role === 'user' ? 'text-right' : 'text-left'}>
            <div className={`inline-block p-2 rounded ${m.role === 'user' ? 'bg-blue-100' : 'bg-gray-100'}`}>{m.text}</div>
          </div>
        ))}
      </div>
      <div className="flex gap-2">
        <input className="flex-1 border rounded p-2" value={input} onChange={e => setInput(e.target.value)} onKeyDown={e => { if (e.key === 'Enter') send() }} />
        <button className="px-4 py-2 bg-blue-600 text-white rounded" onClick={send} disabled={loading}>{loading ? '...' : 'Send'}</button>
      </div>
    </div>
  )
}
