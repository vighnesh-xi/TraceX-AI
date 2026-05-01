import React from 'react'
import useUIStore from '../../store/useUIStore'
import useChatStore from '../../store/useChatStore'

export function Topbar() {
  const { theme, toggleTheme } = useUIStore()
  const togglePanel = useChatStore(s => s.togglePanel)
  const panelOpen = useChatStore(s => s.panelOpen)

  return (
    <header style={{
      height: 'var(--topbar-height)', background: 'var(--bg-secondary)',
      borderBottom: '1px solid var(--border)', display: 'flex',
      alignItems: 'center', justifyContent: 'space-between',
      padding: '0 20px', flexShrink: 0
    }}>
      {/* Left */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        <span style={{ fontWeight: 600, fontSize: 15, color: 'var(--text-primary)' }}>
          AI Codebase Assistant
        </span>
        <span style={{
          fontSize: 10, padding: '2px 8px', letterSpacing: 0.8,
          background: 'var(--accent-light)', color: 'var(--accent)',
          borderRadius: 20, fontWeight: 700
        }}>BETA</span>
      </div>

      {/* Right — Logo + buttons */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
        <button onClick={toggleTheme} style={{
          padding: '6px 14px', borderRadius: 6, background: 'var(--bg-tertiary)',
          color: 'var(--text-secondary)', border: '1px solid var(--border)',
          fontSize: 13, transition: 'all 0.15s'
        }}>
          {theme === 'dark' ? 'Light Mode' : 'Dark Mode'}
        </button>

        <button onClick={() => togglePanel()} style={{
          padding: '6px 14px', borderRadius: 6, fontSize: 13, transition: 'all 0.15s',
          background: panelOpen ? 'var(--accent-light)' : 'var(--bg-tertiary)',
          color: panelOpen ? 'var(--accent)' : 'var(--text-secondary)',
          border: `1px solid ${panelOpen ? 'var(--accent)' : 'var(--border)'}`,
        }}>
          {panelOpen ? 'Hide Panel' : 'Context Panel'}
        </button>

        {/* TraceX AI Logo */}
        <div style={{
          display: 'flex', alignItems: 'center', gap: 8,
          padding: '6px 12px', borderRadius: 8,
          background: 'linear-gradient(135deg, #7c3aed, #4f46e5)',
          boxShadow: '0 2px 12px rgba(124,58,237,0.4)'
        }}>
          {/* Icon mark */}
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
            <path d="M12 2L2 7l10 5 10-5-10-5z" stroke="#fff" strokeWidth="1.8" strokeLinejoin="round"/>
            <path d="M2 17l10 5 10-5" stroke="#fff" strokeWidth="1.8" strokeLinejoin="round" strokeOpacity="0.7"/>
            <path d="M2 12l10 5 10-5" stroke="#fff" strokeWidth="1.8" strokeLinejoin="round" strokeOpacity="0.4"/>
          </svg>
          <div>
            <div style={{ fontSize: 12, fontWeight: 800, color: '#fff', letterSpacing: 0.5, lineHeight: 1.1 }}>
              TraceX
            </div>
            <div style={{ fontSize: 9, fontWeight: 600, color: 'rgba(255,255,255,0.7)', letterSpacing: 1.5, lineHeight: 1 }}>
              AI
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}