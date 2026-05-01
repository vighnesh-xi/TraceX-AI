import React from 'react'
import useUIStore from '../../store/useUIStore'

export function ToastContainer() {
  const toasts = useUIStore(s => s.toasts)

  return (
    <div style={{
      position: 'fixed', bottom: 24, right: 24,
      display: 'flex', flexDirection: 'column', gap: 8, zIndex: 2000
    }}>
      {toasts.map(t => (
        <div key={t.id} style={{
          padding: '10px 18px', borderRadius: 8, fontSize: 13, fontWeight: 500,
          background: t.type === 'error' ? 'var(--error)' : t.type === 'success' ? 'var(--success)' : 'var(--accent)',
          color: '#fff', boxShadow: 'var(--shadow)', minWidth: 220
        }}>
          {t.msg}
        </div>
      ))}
    </div>
  )
}