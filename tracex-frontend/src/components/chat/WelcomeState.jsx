import React from 'react'
import useChatStore from '../../store/useChatStore'
import { useChat } from '../../hooks/useChat'
import { QUERY_TYPES } from '../../utils/queryTypes'

const SUGGESTIONS = [
  { type: 'explain',  text: 'Explain the overall architecture of this codebase' },
  { type: 'flow',     text: 'Trace the data flow from API request to database' },
  { type: 'navigate', text: 'Where is the authentication logic handled?' },
  { type: 'impact',   text: 'What breaks if I change the User model?' },
]

export function WelcomeState() {
  const { sendMessage } = useChat()
  const createSession = useChatStore(s => s.createSession)

  const handle = (s) => {
    createSession('Quick Query')
    sendMessage(s.text, s.type)
  }

  return (
    <div style={{
      display: 'flex', flexDirection: 'column', alignItems: 'center',
      justifyContent: 'center', height: '100%', gap: 28, padding: 40
    }}>
      <div style={{ textAlign: 'center' }}>
        {/* Logo mark */}
        <div style={{
          width: 64, height: 64, borderRadius: 16,
          background: 'linear-gradient(135deg, #7c3aed, #4f46e5)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          margin: '0 auto 16px',
          boxShadow: '0 4px 24px rgba(124,58,237,0.4)'
        }}>
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
            <path d="M12 2L2 7l10 5 10-5-10-5z" stroke="#fff" strokeWidth="1.8" strokeLinejoin="round"/>
            <path d="M2 17l10 5 10-5" stroke="#fff" strokeWidth="1.8" strokeLinejoin="round" strokeOpacity="0.7"/>
            <path d="M2 12l10 5 10-5" stroke="#fff" strokeWidth="1.8" strokeLinejoin="round" strokeOpacity="0.4"/>
          </svg>
        </div>
        <h2 style={{ fontSize: 26, fontWeight: 800, marginBottom: 6, color: 'var(--text-primary)', letterSpacing: 0.3 }}>
          TraceX AI
        </h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: 14, maxWidth: 420, lineHeight: 1.6 }}>
          Ingest your repository and ask anything about your codebase. Powered by hybrid RAG and AST-aware parsing.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, width: '100%', maxWidth: 580 }}>
        {SUGGESTIONS.map((s, i) => (
          <button key={i} onClick={() => handle(s)} style={{
            padding: '16px', borderRadius: 'var(--radius-lg)',
            background: 'var(--bg-secondary)', border: '1px solid var(--border)',
            color: 'var(--text-primary)', textAlign: 'left',
            transition: 'border-color 0.2s', cursor: 'pointer'
          }}
            onMouseEnter={e => e.currentTarget.style.borderColor = 'var(--accent)'}
            onMouseLeave={e => e.currentTarget.style.borderColor = 'var(--border)'}
          >
            <div style={{
              fontSize: 10, fontWeight: 700, color: 'var(--accent)',
              marginBottom: 8, letterSpacing: 1
            }}>
              {s.type.toUpperCase()}
            </div>
            <div style={{ fontSize: 13, color: 'var(--text-secondary)', lineHeight: 1.55 }}>{s.text}</div>
          </button>
        ))}
      </div>
    </div>
  )
}