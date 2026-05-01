import { apiPost } from './client'

export const ingestRepo = (body) => apiPost('/index', body)