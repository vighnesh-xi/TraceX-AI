import React from 'react'

export function RefsTab({ refs = [] }) {
  if (!refs.length) return <p style={{ fontSize: 13, color: 'var(--text-muted)' }}>No references found.</p>
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
      {refs.map((r, i) => (
        <div key={i} style={{
          padding: '10px 12px', background: 'var(--bg-tertiary)',
          borderRadius: 6, border: '1px solid var(--border)'
        }}>
          <div style={{ fontSize: 12, fontFamily: 'monospace', color: 'var(--accent)', marginBottom: 4 }}>
            📄 {r.file}
          </div>
          <pre style={{ fontSize: 12, color: 'var(--text-secondary)', whiteSpace: 'pre-wrap', margin: 0 }}>
            {r.snippet}
          </pre>
        </div>
      ))}
    </div>
  )
}