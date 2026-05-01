export function formatAnswer(raw) {
  if (!raw) return ''
  if (typeof raw === 'object') return JSON.stringify(raw, null, 2)
  return String(raw)
}