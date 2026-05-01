import React, { useState } from 'react'
import useUIStore from '../../store/useUIStore'
import { useIngest } from '../../hooks/useIngest'

const TABS = ['Local Path', 'GitHub URL']

export function IngestModal() {
  const { ingestModalOpen, closeIngestModal } = useUIStore()
  const { ingest, loading, status } = useIngest()
  const [tab, setTab] = useState('Local Path')
  const [localPath, setLocalPath] = useState('')
  const [githubUrl, setGithubUrl] = useState('')

  if (!ingestModalOpen) return null

  const value = tab === 'Local Path' ? localPath : githubUrl
  const canSubmit = value.trim() && !loading

  const handleSubmit = () => {
    if (!canSubmit) return
    ingest(value.trim(), tab === 'GitHub URL')
  }

  const handleKey = (e) => {
    if (e.key === 'Enter') handleSubmit()
  }

  return (
    <div onClick={closeIngestModal} style={{
      position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.65)',
      display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000
    }}>
      <div onClick={e => e.stopPropagation()} style={{
        background: 'var(--bg-secondary)', borderRadius: 'var(--radius-lg)',
        border: '1px solid var(--border)', padding: '28px 32px', width: 500,
        boxShadow: 'var(--shadow)'
      }}>
        <h2 style={{ fontSize: 18, fontWeight: 700, color: 'var(--text-primary)', marginBottom: 4 }}>
          Ingest Repository
        </h2>
        <p style={{ fontSize: 13, color: 'var(--text-secondary)', marginBottom: 20, lineHeight: 1.5 }}>
          Index a local repository or a public GitHub repository.
        </p>

        {/* Tabs */}
        <div style={{
          display: 'flex', marginBottom: 18,
          background: 'var(--bg-tertiary)', borderRadius: 6, padding: 3
        }}>
          {TABS.map(t => (
            <button key={t} onClick={() => setTab(t)} style={{
              flex: 1, padding: '7px 0', borderRadius: 4,
              fontSize: 13, fontWeight: 600, cursor: 'pointer',
              background: tab === t ? 'var(--bg-secondary)' : 'transparent',
              color: tab === t ? 'var(--text-primary)' : 'var(--text-muted)',
              border: tab === t ? '1px solid var(--border)' : 'none',
              transition: 'all 0.15s'
            }}>
              {t}
            </button>
          ))}
        </div>

        {/* Input */}
        <label style={{ fontSize: 12, color: 'var(--text-muted)', display: 'block', marginBottom: 6, fontWeight: 600 }}>
          {tab === 'Local Path' ? 'Absolute path to repository' : 'Public GitHub repository URL'}
        </label>
        <input
          key={tab}
          value={tab === 'Local Path' ? localPath : githubUrl}
          onChange={e => tab === 'Local Path' ? setLocalPath(e.target.value) : setGithubUrl(e.target.value)}
          onKeyDown={handleKey}
          autoFocus
          placeholder={tab === 'Local Path' ? 'D:\\Projects\\my-repo  or  /home/user/my-repo' : 'https://github.com/username/repository'}
          style={{
            width: '100%', padding: '10px 14px', borderRadius: 'var(--radius)',
            background: 'var(--bg-tertiary)', border: '1px solid var(--border)',
            color: 'var(--text-primary)', fontSize: 14, outline: 'none',
            transition: 'border-color 0.2s', marginBottom: 8
          }}
          onFocus={e => e.target.style.borderColor = 'var(--accent)'}
          onBlur={e => e.target.style.borderColor = 'var(--border)'}
        />
        <p style={{ fontSize: 11, color: 'var(--text-muted)', marginBottom: 16 }}>
          Press Enter or click Index Repository to start.
        </p>

        {status && (
          <div style={{
            padding: '10px 14px', borderRadius: 6, marginBottom: 16, fontSize: 13,
            background: status.type === 'success' ? 'rgba(63,185,80,0.1)' : 'rgba(248,81,73,0.1)',
            color: status.type === 'success' ? 'var(--success)' : 'var(--error)',
            border: `1px solid ${status.type === 'success' ? 'var(--success)' : 'var(--error)'}`
          }}>
            {status.msg}
          </div>
        )}

        <div style={{ display: 'flex', gap: 10, justifyContent: 'flex-end' }}>
          <button onClick={closeIngestModal} style={{
            padding: '9px 18px', borderRadius: 'var(--radius)', fontSize: 13,
            background: 'var(--bg-tertiary)', color: 'var(--text-secondary)',
            border: '1px solid var(--border)', cursor: 'pointer'
          }}>
            Cancel
          </button>
          <button onClick={handleSubmit} disabled={!canSubmit} style={{
            padding: '9px 20px', borderRadius: 'var(--radius)', fontSize: 13,
            fontWeight: 600, border: 'none', transition: 'all 0.2s',
            background: !canSubmit ? 'var(--bg-tertiary)' : 'var(--accent)',
            color: !canSubmit ? 'var(--text-muted)' : '#fff',
            cursor: loading ? 'wait' : !canSubmit ? 'not-allowed' : 'pointer'
          }}>
            {loading ? 'Indexing...' : 'Index Repository'}
          </button>
        </div>
      </div>
    </div>
  )
}