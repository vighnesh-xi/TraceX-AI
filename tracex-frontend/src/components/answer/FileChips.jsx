import React from 'react'

export function FileChips({ files = [] }) {
  if (!files.length) return null
  return (
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginTop: 8 }}>
      {files.map((f, i) => (
        <span key={i} style={{
          fontSize: 11, padding: '3px 10px', borderRadius: 20,
          background: 'var(--bg-tertiary)', color: 'var(--text-secondary)',
          border: '1px solid var(--border)', fontFamily: 'monospace'
        }}>
          {f}
        </span>
      ))}
    </div>
  )
}