import React from 'react'

export function Badge({ label, color = 'accent' }) {
  const colors = {
    accent:  { bg: 'var(--accent-light)',        text: 'var(--accent)' },
    success: { bg: 'rgba(63,185,80,0.15)',       text: 'var(--success)' },
    error:   { bg: 'rgba(248,81,73,0.15)',       text: 'var(--error)' },
    warning: { bg: 'rgba(210,153,34,0.15)',      text: 'var(--warning)' },
  }
  const c = colors[color] || colors.accent
  return (
    <span style={{
      fontSize: 11, fontWeight: 700, padding: '2px 8px',
      borderRadius: 20, background: c.bg, color: c.text
    }}>
      {label}
    </span>
  )
}