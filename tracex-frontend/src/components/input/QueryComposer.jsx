import React, { useState } from 'react'
import { useChat } from '../../hooks/useChat'
import useChatStore from '../../store/useChatStore'
import { TopKSelector } from './TopKSelector'
import { QUERY_TYPES } from '../../utils/queryTypes'

export function QueryComposer() {
  const [query, setQuery] = useState('')
  const [queryType, setQueryType] = useState('explain')
  const [topK, setTopK] = useState(5)
  const { sendMessage } = useChat()
  const isLoading = useChatStore(s => s.isLoading)
  const createSession = useChatStore(s => s.createSession)
  const activeSessionId = useChatStore(s => s.activeSessionId)

  const handleSubmit = async (e) => {
    e?.preventDefault()
    if (!query.trim() || isLoading) return
    if (!activeSessionId) createSession('Chat')
    const q = query.trim()
    setQuery('')
    await sendMessage(q, queryType, topK)
  }

  const handleKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div style={{
      padding: '12px 20px 20px', background: 'var(--bg-primary)',
      borderTop: '1px solid var(--border)', flexShrink: 0
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
        <div style={{ display: 'flex', gap: 6 }}>
          {QUERY_TYPES.map(t => (
            <button key={t.id} onClick={() => setQueryType(t.id)} style={{
              padding: '4px 14px', borderRadius: 20, fontSize: 12, fontWeight: 600,
              background: queryType === t.id ? 'var(--accent)' : 'var(--bg-tertiary)',
              color: queryType === t.id ? '#fff' : 'var(--text-secondary)',
              border: queryType === t.id ? 'none' : '1px solid var(--border)',
              transition: 'all 0.15s', cursor: 'pointer'
            }}>
              {t.label}
            </button>
          ))}
        </div>
        <TopKSelector value={topK} onChange={setTopK} />
      </div>

      <form onSubmit={handleSubmit} style={{ display: 'flex', gap: 10 }}>
        <textarea
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={handleKey}
          placeholder="Ask anything about your codebase... (Enter to send, Shift+Enter for newline)"
          rows={2}
          style={{
            flex: 1, padding: '10px 14px', borderRadius: 'var(--radius)',
            background: 'var(--bg-secondary)', color: 'var(--text-primary)',
            border: '1px solid var(--border)', outline: 'none',
            resize: 'none', fontSize: 14, lineHeight: 1.5,
            transition: 'border-color 0.2s'
          }}
          onFocus={e => e.target.style.borderColor = 'var(--accent)'}
          onBlur={e => e.target.style.borderColor = 'var(--border)'}
        />
        <button type="submit" disabled={isLoading || !query.trim()} style={{
          padding: '0 22px', borderRadius: 'var(--radius)', fontWeight: 600,
          fontSize: 14, flexShrink: 0, transition: 'all 0.2s',
          background: isLoading || !query.trim() ? 'var(--bg-tertiary)' : 'var(--accent)',
          color: isLoading || !query.trim() ? 'var(--text-muted)' : '#fff',
          border: 'none', cursor: isLoading ? 'wait' : !query.trim() ? 'not-allowed' : 'pointer'
        }}>
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  )
}