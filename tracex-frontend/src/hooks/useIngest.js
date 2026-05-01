import { useState } from 'react'
import { ingestRepo } from '../api/ingest'
import useUIStore from '../store/useUIStore'
import useChatStore from '../store/useChatStore'

export function useIngest() {
  const [loading, setLoading] = useState(false)
  const [status, setStatus] = useState(null)
  const addToast = useUIStore(s => s.addToast)
  const setRepoIngested = useChatStore(s => s.setRepoIngested)
  const closeIngestModal = useUIStore(s => s.closeIngestModal)

  const ingest = async (value, isGithub = false) => {
    setLoading(true)
    setStatus(null)
    try {
      const body = isGithub ? { github_url: value } : { repo_path: value }
      const data = await ingestRepo(body)
      const msg = `Indexed: ${data.total_files} files, ${data.total_chunks} chunks.`
      setStatus({ type: 'success', msg })
      setRepoIngested(true)
      addToast('Repository indexed successfully', 'success')
      setTimeout(closeIngestModal, 2000)
    } catch (err) {
      setStatus({ type: 'error', msg: err.message })
      addToast(err.message, 'error')
    } finally {
      setLoading(false)
    }
  }

  return { ingest, loading, status }
}