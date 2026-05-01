import React from 'react'
import { TypingIndicator } from './TypingIndicator'

function renderInline(text) {
  const parts = text.split(/(`[^`]+`|\*\*[^*]+\*\*)/g)
  return parts.map((part, i) => {
    if (part.startsWith('`') && part.endsWith('`')) {
      return (
        <code key={i} style={{
          fontFamily: 'monospace', fontSize: 13,
          background: 'var(--bg-hover)', padding: '1px 5px',
          borderRadius: 3, color: 'var(--text-primary)'
        }}>
          {part.slice(1, -1)}
        </code>
      )
    }
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={i} style={{ color: 'var(--text-primary)', fontWeight: 700 }}>{part.slice(2, -2)}</strong>
    }
    return part
  })
}

function renderLines(lines) {
  return lines.map((line, i) => {
    const trimmed = line.trim()
    if (trimmed === '') return <div key={i} style={{ height: 6 }} />

    const numberedMatch = trimmed.match(/^(\d+)\.\s+(.*)/)
    if (numberedMatch) {
      return (
        <div key={i} style={{ display: 'flex', gap: 10, marginBottom: 7, alignItems: 'flex-start' }}>
          <span style={{ color: 'var(--accent)', fontWeight: 700, flexShrink: 0, minWidth: 18, lineHeight: 1.7 }}>
            {numberedMatch[1]}.
          </span>
          <span style={{ lineHeight: 1.7, color: 'var(--text-primary)' }}>
            {renderInline(numberedMatch[2])}
          </span>
        </div>
      )
    }

    if (trimmed.startsWith('- ')) {
      return (
        <div key={i} style={{ display: 'flex', gap: 8, marginBottom: 5, paddingLeft: 4, alignItems: 'flex-start' }}>
          <span style={{ color: 'var(--accent)', flexShrink: 0, marginTop: 3, fontSize: 11 }}>—</span>
          <span style={{ lineHeight: 1.7, color: 'var(--text-primary)' }}>
            {renderInline(trimmed.slice(2))}
          </span>
        </div>
      )
    }

    return (
      <div key={i} style={{ marginBottom: 4, lineHeight: 1.75, color: 'var(--text-primary)' }}>
        {renderInline(line)}
      </div>
    )
  })
}

function parseSections(text) {
  if (!text) return []
  const lines = text.split('\n')
  const sections = []
  let current = null

  for (const line of lines) {
    const trimmed = line.trim()
    const headingMatch = trimmed.match(/^\*\*(.+)\*\*$/)
    if (headingMatch) {
      if (current) sections.push(current)
      current = { label: headingMatch[1], lines: [] }
    } else {
      if (!current) current = { label: null, lines: [] }
      current.lines.push(line)
    }
  }
  if (current) sections.push(current)
  return sections.filter(s => s.lines.some(l => l.trim() !== ''))
}

function SectionCard({ label, lines }) {
  return (
    <div style={{
      borderRadius: 'var(--radius)', background: 'var(--bg-tertiary)',
      border: '1px solid var(--border)', overflow: 'hidden', marginBottom: 10
    }}>
      {label && (
        <div style={{
          padding: '8px 14px', background: 'var(--bg-hover)',
          borderBottom: '1px solid var(--border)',
          fontSize: 11, fontWeight: 700, color: 'var(--accent)', letterSpacing: 1
        }}>
          {label.toUpperCase()}
        </div>
      )}
      <div style={{ padding: '12px 14px', fontSize: 14 }}>
        {renderLines(lines)}
      </div>
    </div>
  )
}

export function BotMessage({ content, loading, error }) {
  const sections = parseSections(content)

  return (
    <div style={{ display: 'flex', justifyContent: 'flex-start', marginBottom: 20 }}>
      <div style={{ maxWidth: '84%', width: '100%' }}>
        <div style={{
          fontSize: 11, color: 'var(--text-muted)', marginBottom: 6,
          fontWeight: 600, letterSpacing: 0.3
        }}>
          TRACEX AI
        </div>
        {loading ? (
          <TypingIndicator />
        ) : error ? (
          <div style={{
            padding: '14px 18px', borderRadius: 'var(--radius-lg)',
            background: 'rgba(248,81,73,0.08)', color: 'var(--error)',
            border: '1px solid var(--error)', fontSize: 14, lineHeight: 1.7
          }}>
            {content}
          </div>
        ) : (
          <div>
            {sections.map((s, i) => (
              <SectionCard key={i} label={s.label} lines={s.lines} />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}