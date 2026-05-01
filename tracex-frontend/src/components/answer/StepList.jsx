import React from 'react'

export function StepList({ steps = [] }) {
  if (!steps.length) return null
  return (
    <ol style={{ marginTop: 10, paddingLeft: 20 }}>
      {steps.map((s, i) => (
        <li key={i} style={{ fontSize: 13, color: 'var(--text-primary)', marginBottom: 8, lineHeight: 1.6, paddingLeft: 4 }}>
          {s}
        </li>
      ))}
    </ol>
  )
}