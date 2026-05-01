import React from 'react'
import useChatStore from '../../store/useChatStore'
import useUIStore from '../../store/useUIStore'

export function Sidebar() {
  const { sessions, activeSessionId, createSession, setActiveSession, repoIngested } = useChatStore()
  const openIngestModal = useUIStore(s => s.openIngestModal)

  const formatTime = (date) => new Date(date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })

  return (
    <aside style={{
      width: 'var(--sidebar-width)', background: 'var(--bg-secondary)',
      borderRight: '1px solid var(--border)', display: 'flex',
      flexDirection: 'column', height: '100dvh', flexShrink: 0
    }}>
      {/* Logo */}
      <div style={{ padding: '16px 18px', borderBottom: '1px solid var(--border)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <div style={{
            width: 36, height: 36, borderRadius: 9,
            background: 'linear-gradient(135deg, #7c3aed, #4f46e5)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            boxShadow: '0 2px 10px rgba(124,58,237,0.4)', flexShrink: 0
          }}>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
              <path d="M12 2L2 7l10 5 10-5-10-5z" stroke="#fff" strokeWidth="1.8" strokeLinejoin="round"/>
              <path d="M2 17l10 5 10-5" stroke="#fff" strokeWidth="1.8" strokeLinejoin="round" strokeOpacity="0.7"/>
              <path d="M2 12l10 5 10-5" stroke="#fff" strokeWidth="1.8" strokeLinejoin="round" strokeOpacity="0.4"/>
            </svg>
          </div>
          <div>
            <div style={{ fontWeight: 800, fontSize: 15, color: 'var(--text-primary)', lineHeight: 1.15, letterSpacing: 0.3 }}>
              TraceX AI
            </div>
            <div style={{ fontSize: 10, color: 'var(--text-muted)', letterSpacing: 0.5 }}>
              AI CODEBASE ASSISTANT
            </div>
          </div>
        </div>
      </div>

      {/* Repo Status */}
      <div style={{ padding: '14px 14px 0' }}>
        <div style={{
          padding: '12px 14px', borderRadius: 'var(--radius)', marginBottom: 10,
          background: repoIngested ? 'rgba(63,185,80,0.08)' : 'var(--bg-tertiary)',
          border: `1px solid ${repoIngested ? 'rgba(63,185,80,0.3)' : 'var(--border)'}`,
        }}>
          <div style={{ fontSize: 11, color: 'var(--text-muted)', marginBottom: 5, fontWeight: 600, letterSpacing: 0.5 }}>
            REPOSITORY STATUS
          </div>
          <div style={{
            display: 'flex', alignItems: 'center', gap: 7, fontSize: 13,
            color: repoIngested ? 'var(--success)' : 'var(--text-secondary)', fontWeight: 600
          }}>
            <span style={{
              width: 7, height: 7, borderRadius: '50%', flexShrink: 0,
              background: repoIngested ? 'var(--success)' : 'var(--text-muted)',
              display: 'inline-block'
            }} />
            {repoIngested ? 'Indexed and Ready' : 'No Repository Indexed'}
          </div>
          {!repoIngested && (
            <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 4 }}>
              Ingest a repo to start querying
            </div>
          )}
        </div>

        <button onClick={openIngestModal} style={{
          width: '100%', padding: '9px 14px', borderRadius: 'var(--radius)',
          background: 'var(--accent)', color: '#fff', border: 'none',
          fontWeight: 600, fontSize: 13, transition: 'background 0.2s',
          cursor: 'pointer', marginBottom: 8
        }}
          onMouseEnter={e => e.currentTarget.style.background = 'var(--accent-hover)'}
          onMouseLeave={e => e.currentTarget.style.background = 'var(--accent)'}
        >
          {repoIngested ? 'Re-index Repository' : '+ Ingest Repository'}
        </button>

        <button onClick={() => createSession()} style={{
          width: '100%', padding: '8px 14px', borderRadius: 'var(--radius)',
          background: 'transparent', color: 'var(--text-secondary)',
          fontSize: 13, textAlign: 'left', border: '1px solid var(--border)',
          transition: 'all 0.15s', cursor: 'pointer'
        }}
          onMouseEnter={e => { e.currentTarget.style.background = 'var(--bg-tertiary)'; e.currentTarget.style.color = 'var(--text-primary)' }}
          onMouseLeave={e => { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.color = 'var(--text-secondary)' }}
        >
          + New Chat
        </button>
      </div>

      {/* Chat History */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '12px 10px 8px' }}>
        <div style={{
          fontSize: 11, color: 'var(--text-muted)', fontWeight: 600,
          letterSpacing: 0.5, padding: '0 6px', marginBottom: 8
        }}>
          CHAT HISTORY
        </div>

        {sessions.length === 0 ? (
          <div style={{
            padding: '14px 12px', borderRadius: 6,
            background: 'var(--bg-tertiary)', border: '1px dashed var(--border)', textAlign: 'center'
          }}>
            <div style={{ fontSize: 12, color: 'var(--text-muted)', lineHeight: 1.7 }}>
              No conversations yet.<br />Ingest a repository and start asking questions.
            </div>
          </div>
        ) : sessions.map(s => (
          <button key={s.id} onClick={() => setActiveSession(s.id)} style={{
            width: '100%', padding: '9px 10px', borderRadius: 6, textAlign: 'left',
            background: activeSessionId === s.id ? 'var(--accent-light)' : 'transparent',
            border: 'none',
            borderLeft: `2px solid ${activeSessionId === s.id ? 'var(--accent)' : 'transparent'}`,
            marginBottom: 2, cursor: 'pointer', transition: 'all 0.15s'
          }}>
            <div style={{
              fontSize: 13, fontWeight: activeSessionId === s.id ? 600 : 400,
              color: activeSessionId === s.id ? 'var(--text-primary)' : 'var(--text-secondary)',
              overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', marginBottom: 2
            }}>
              {s.name}
            </div>
            <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>{formatTime(s.createdAt)}</div>
          </button>
        ))}
      </div>

      {/* Footer */}
      <div style={{
        padding: '12px 18px', borderTop: '1px solid var(--border)',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between'
      }}>
        <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>TraceX AI v1.0.0</div>
        <div style={{ fontSize: 11, color: 'var(--text-muted)', fontStyle: 'italic' }}>by Vighnesh</div>
      </div>
    </aside>
  )
}