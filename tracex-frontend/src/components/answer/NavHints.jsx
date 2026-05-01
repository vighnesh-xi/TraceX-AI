import React from 'react'

export function NavHints({ hints = [] }) {
  if (!hints.length) return null
  return (
    <ul style={{ marginTop: 10, paddingLeft: 18 }}>
      {hints.map((h, i) => (
        <li key={i} style={{ fontSize: 13, color: 'var(--text-secondary)', marginBottom: 4, lineHeight: 1.6 }}>
          {h}
        </li>
      ))}
    </ul>
  )
}