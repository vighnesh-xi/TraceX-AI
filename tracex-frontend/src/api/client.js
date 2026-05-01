const BASE = 'http://localhost:8000/api/v1'

function extractMessage(data) {
  if (!data) return 'Unknown error'
  if (typeof data.detail === 'string') return data.detail
  if (Array.isArray(data.detail)) return data.detail.map(e => e.msg || JSON.stringify(e)).join(', ')
  if (typeof data.detail === 'object') return JSON.stringify(data.detail)
  if (typeof data.message === 'string') return data.message
  return JSON.stringify(data)
}

export async function apiPost(endpoint, body) {
  const res = await fetch(`${BASE}${endpoint}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  const data = await res.json()
  if (!res.ok) throw new Error(extractMessage(data))
  return data
}

export async function apiGet(endpoint) {
  const res = await fetch(`${BASE}${endpoint}`)
  const data = await res.json()
  if (!res.ok) throw new Error(extractMessage(data))
  return data
}