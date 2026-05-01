import useChatStore from '../store/useChatStore'
import useUIStore from '../store/useUIStore'
import { sendQuery } from '../api/query'

export function useChat() {
  const { addMessage, updateLastMessage, setLoading, createSession, activeSessionId, togglePanel } = useChatStore()
  const addToast = useUIStore(s => s.addToast)

  const sendMessage = async (query, queryType = 'explain', topK = 5) => {
    if (!activeSessionId) createSession()
    addMessage({ role: 'user', content: query })
    setLoading(true)
    addMessage({ role: 'assistant', content: '', loading: true })

    try {
      const data = await sendQuery(query, queryType, topK)
      const answer = data.answer || data.response || JSON.stringify(data)
      updateLastMessage({ content: answer, loading: false })

      togglePanel({
        references: data.references || [],
        stats: {
          query_type: data.query_type || queryType,
          chunks_retrieved: data.references?.length ?? topK,
          top_k: topK,
          navigation_hints: data.navigation_hints?.length ?? 0,
        }
      })
    } catch (err) {
      updateLastMessage({ content: `Error: ${err.message}`, loading: false, error: true })
      addToast(err.message, 'error')
    } finally {
      setLoading(false)
    }
  }

  return { sendMessage }
}