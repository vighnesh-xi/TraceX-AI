import React from 'react'

export function TypingIndicator() {
  return (
    <div style={{
      display: 'inline-flex', alignItems: 'center', gap: 8,
      padding: '12px 16px', borderRadius: 'var(--radius-lg)',
      background: 'var(--bg-secondary)', border: '1px solid var(--border)'
    }}>
      <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>CodeLens is thinking</span>
      {[0, 1, 2].map(i => (
        <span key={i} style={{
          width: 6, height: 6, borderRadius: '50%', background: 'var(--accent)',
          display: 'inline-block',
          animation: `bounce 1.2s ${i * 0.2}s infinite ease-in-out`
        }} />
      ))}
    </div>
  )
}