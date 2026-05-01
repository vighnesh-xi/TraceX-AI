import React from 'react'

export function AnswerSection({ content }) {
  return (
    <div style={{
      padding: '12px 16px', background: 'var(--bg-secondary)',
      borderRadius: 'var(--radius-lg)', border: '1px solid var(--border)',
      fontSize: 14, lineHeight: 1.7, color: 'var(--text-primary)', whiteSpace: 'pre-wrap'
    }}>
      {content}
    </div>
  )
}