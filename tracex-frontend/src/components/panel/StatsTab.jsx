import React from 'react'

export function StatsTab({ stats }) {
  if (!stats) return <p style={{ fontSize: 13, color: 'var(--text-muted)' }}>No stats available yet.</p>
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
      {Object.entries(stats).map(([k, v]) => (
        <div key={k} style={{
          display: 'flex', justifyContent: 'space-between', alignItems: 'center',
          padding: '8px 12px', background: 'var(--bg-tertiary)', borderRadius: 6
        }}>
          <span style={{ fontSize: 13, color: 'var(--text-secondary)', textTransform: 'capitalize' }}>
            {k.replace(/_/g, ' ')}
          </span>
          <span style={{ fontSize: 13, fontWeight: 600, color: 'var(--text-primary)' }}>{String(v)}</span>
        </div>
      ))}
    </div>
  )
}