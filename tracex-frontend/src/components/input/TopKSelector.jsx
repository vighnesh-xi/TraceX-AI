import React from 'react'

export function TopKSelector({ value, onChange }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
      <label style={{ fontSize: 12, color: 'var(--text-muted)' }}>Top-K</label>
      <select value={value} onChange={e => onChange(Number(e.target.value))} style={{
        padding: '4px 8px', borderRadius: 6, fontSize: 12,
        background: 'var(--bg-tertiary)', color: 'var(--text-primary)',
        border: '1px solid var(--border)', outline: 'none', cursor: 'pointer'
      }}>
        {[3, 5, 10, 15].map(k => <option key={k} value={k}>{k}</option>)}
      </select>
    </div>
  )
}