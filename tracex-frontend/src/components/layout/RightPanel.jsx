import React, { useState } from 'react'
import useChatStore from '../../store/useChatStore'

const TABS = ['References', 'Stats']

export function RightPanel() {
  const panelContent = useChatStore(s => s.panelContent)
  const [tab, setTab] = useState('References')

  const refs = panelContent?.references || []
  const stats = panelContent?.stats || null

  return (
    <aside style={{
      width: 'var(--panel-width)', background: 'var(--bg-secondary)',
      borderLeft: '1px solid var(--border)', display: 'flex',
      flexDirection: 'column', flexShrink: 0
    }}>
      <div style={{ padding: '14px 16px', borderBottom: '1px solid var(--border)', flexShrink: 0 }}>
        <div style={{ fontSize: 13, fontWeight: 700, color: 'var(--text-primary)', marginBottom: 3 }}>
          Context Panel
        </div>
        <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>
          Files and chunks used to generate the answer
        </div>
      </div>

      <div style={{ display: 'flex', borderBottom: '1px solid var(--border)', flexShrink: 0 }}>
        {TABS.map(t => (
          <button key={t} onClick={() => setTab(t)} style={{
            flex: 1, padding: '10px 0', fontSize: 12, fontWeight: 600,
            color: tab === t ? 'var(--accent)' : 'var(--text-muted)',
            background: 'none', border: 'none',
            borderBottom: `2px solid ${tab === t ? 'var(--accent)' : 'transparent'}`,
            cursor: 'pointer', transition: 'all 0.15s'
          }}>
            {t}
          </button>
        ))}
      </div>

      <div style={{ flex: 1, overflowY: 'auto', padding: '14px' }}>
        {!panelContent ? (
          <div style={{
            padding: 20, borderRadius: 8, background: 'var(--bg-tertiary)',
            border: '1px dashed var(--border)', textAlign: 'center'
          }}>
            <div style={{ fontSize: 28, color: 'var(--text-muted)', marginBottom: 10 }}>[ ]</div>
            <div style={{ fontSize: 12, color: 'var(--text-muted)', lineHeight: 1.7 }}>
              Ask a question to see which files and code chunks the AI used to generate its answer.
            </div>
          </div>
        ) : tab === 'References' ? (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            {refs.length === 0 ? (
              <p style={{ fontSize: 13, color: 'var(--text-muted)' }}>No file references returned for this query.</p>
            ) : refs.map((r, i) => (
              <div key={i} style={{
                borderRadius: 6, background: 'var(--bg-tertiary)',
                border: '1px solid var(--border)', overflow: 'hidden'
              }}>
                <div style={{
                  padding: '8px 12px', background: 'var(--bg-hover)',
                  borderBottom: '1px solid var(--border)',
                  display: 'flex', justifyContent: 'space-between', alignItems: 'center'
                }}>
                  <span style={{ fontSize: 12, fontFamily: 'monospace', color: 'var(--accent)', fontWeight: 600 }}>
                    {r.file || r.file_path || 'Unknown file'}
                  </span>
                  {r.score != null && (
                    <span style={{
                      fontSize: 10, padding: '2px 7px', borderRadius: 10,
                      background: 'var(--accent-light)', color: 'var(--accent)', fontWeight: 700
                    }}>
                      {(r.score * 100).toFixed(0)}% match
                    </span>
                  )}
                </div>
                {r.snippet && (
                  <pre style={{
                    margin: 0, padding: '10px 12px', fontSize: 11,
                    color: 'var(--text-secondary)', whiteSpace: 'pre-wrap',
                    lineHeight: 1.6, maxHeight: 140, overflowY: 'auto'
                  }}>
                    {r.snippet}
                  </pre>
                )}
              </div>
            ))}
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {!stats ? (
              <p style={{ fontSize: 13, color: 'var(--text-muted)' }}>No stats available.</p>
            ) : Object.entries(stats).map(([k, v]) => (
              <div key={k} style={{
                display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                padding: '9px 12px', background: 'var(--bg-tertiary)', borderRadius: 6
              }}>
                <span style={{ fontSize: 13, color: 'var(--text-secondary)', textTransform: 'capitalize' }}>
                  {k.replace(/_/g, ' ')}
                </span>
                <span style={{ fontSize: 13, fontWeight: 600, color: 'var(--text-primary)' }}>{String(v)}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </aside>
  )
}