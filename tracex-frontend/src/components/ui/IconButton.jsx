import React from 'react'

export function IconButton({ icon, onClick, title, active = false }) {
  return (
    <button onClick={onClick} title={title} style={{
      width: 34, height: 34, borderRadius: 6,
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      fontSize: 16,
      background: active ? 'var(--accent-light)' : 'var(--bg-tertiary)',
      color: active ? 'var(--accent)' : 'var(--text-secondary)',
      border: `1px solid ${active ? 'var(--accent)' : 'var(--border)'}`,
      transition: 'all 0.15s', cursor: 'pointer'
    }}>
      {icon}
    </button>
  )
}