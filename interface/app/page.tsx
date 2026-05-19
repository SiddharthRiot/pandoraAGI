'use client'

import { useState, useRef, useEffect } from 'react'
import dynamic from 'next/dynamic'

const ParticleNetwork = dynamic(() => import('./components/ParticleNetwork'), { ssr: false })

export default function Home() {
  const [prompt, setPrompt] = useState('')
  const [messages, setMessages] = useState<{role: string, content: string}[]>([])
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const send = async () => {
    if (!prompt.trim()) return
    const userMsg = prompt
    setPrompt('')
    setMessages(prev => [...prev, { role: 'user', content: userMsg }])
    setLoading(true)

    try {
      const res = await fetch('http://localhost:8000/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: userMsg })
      })
      const data = await res.json()
      setMessages(prev => [...prev, { role: 'assistant', content: data.output }])
    } catch {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Error connecting to PandoraAGI core.' }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-black/10 text-white flex flex-col relative z-10">
      <ParticleNetwork />

      <div className="border-b border-zinc-800 px-6 py-4 flex items-center justify-between backdrop-blur-sm bg-black/40">
        <div>
          <h1 className="text-xl font-bold tracking-tight">PandoraAGI</h1>
          <p className="text-xs text-zinc-500">AGI should belong to humanity</p>
        </div>
        <span className="text-xs text-green-500 border border-green-800 px-2 py-1 rounded">v0.0.1 — alive</span>
      </div>

      <div className="flex-1 overflow-y-auto px-6 py-6 space-y-6 max-w-3xl w-full mx-auto">
        {messages.length === 0 && (
          <div className="text-center mt-32">
            <p className="text-zinc-600 text-sm">Send a message to begin.</p>
          </div>
        )}
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-xl px-4 py-3 rounded text-sm leading-relaxed ${
              msg.role === 'user'
                ? 'bg-zinc-800/80 backdrop-blur-sm text-white'
                : 'bg-zinc-900/80 backdrop-blur-sm border border-zinc-800 text-zinc-200'
            }`}>
              {msg.content}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-zinc-900/80 backdrop-blur-sm border border-zinc-800 px-4 py-3 rounded text-sm text-zinc-500">
              thinking...
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="border-t border-zinc-800 px-6 py-4 max-w-3xl w-full mx-auto backdrop-blur-sm bg-black/40">
        <div className="flex gap-3">
          <input
            className="flex-1 bg-zinc-900/80 backdrop-blur-sm border border-zinc-800 rounded px-4 py-2 text-sm text-white placeholder-zinc-600 outline-none focus:border-zinc-600"
            placeholder="Talk to PandoraAGI..."
            value={prompt}
            onChange={e => setPrompt(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && send()}
          />
          <button
            onClick={send}
            disabled={loading}
            className="bg-white text-black px-4 py-2 rounded text-sm font-medium disabled:opacity-40"
          >
            Send
          </button>
        </div>
      </div>
    </main>
  )
}