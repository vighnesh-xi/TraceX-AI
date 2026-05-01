import { apiPost } from './client'

export const sendQuery = (query, query_type = 'explain', top_k = 5) =>
  apiPost('/query', { query, query_type, top_k })