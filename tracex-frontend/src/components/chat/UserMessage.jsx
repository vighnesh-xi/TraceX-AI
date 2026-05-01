import React from 'react'

export function UserMessage({ content }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: 20 }}>
      <div>
        <div style={{
          fontSize: 11, color: 'var(--text-muted)', textAlign: 'right',
          marginBottom: 5, fontWeight: 600, letterSpacing: 0.3
        }}>
          YOU
        </div>
        <div style={{
          padding: '12px 16px', borderRadius: 'var(--radius-lg)',
          background: 'var(--accent)', color: '#fff',
          fontSize: 14, lineHeight: 1.65, maxWidth: 520, whiteSpace: 'pre-wrap'
        }}>
          {content}
        </div>
      </div>
    </div>
  )
}