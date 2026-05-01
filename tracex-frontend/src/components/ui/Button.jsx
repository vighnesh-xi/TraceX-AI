import React from 'react'

export function Button({ children, onClick, disabled, variant = 'primary', style = {} }) {
  const base = {
    padding: '9px 18px', borderRadius: 'var(--radius)', fontSize: 13,
    fontWeight: 600, border: 'none', transition: 'all 0.2s',
    cursor: disabled ? 'not-allowed' : 'pointer'
  }
  const variants = {
    primary: {
      background: disabled ? 'var(--bg-tertiary)' : 'var(--accent)',
      color: disabled ? 'var(--text-muted)' : '#fff'
    },
    ghost: {
      background: 'var(--bg-tertiary)',
      color: 'var(--text-secondary)',
      border: '1px solid var(--border)'
    },
  }
  return (
    <button onClick={onClick} disabled={disabled} style={{ ...base, ...variants[variant], ...style }}>
      {children}
    </button>
  )
}