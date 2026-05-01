import { create } from 'zustand'

const useUIStore = create((set) => ({
  theme: 'dark',
  ingestModalOpen: false,
  toasts: [],

  toggleTheme: () => set(s => {
    const next = s.theme === 'dark' ? 'light' : 'dark'
    document.documentElement.setAttribute('data-theme', next)
    return { theme: next }
  }),

  openIngestModal: () => set({ ingestModalOpen: true }),
  closeIngestModal: () => set({ ingestModalOpen: false }),

  addToast: (msg, type = 'info') => {
    const id = Date.now().toString()
    const safeMsg = typeof msg === 'string' ? msg : JSON.stringify(msg)
    set(s => ({ toasts: [...s.toasts, { id, msg: safeMsg, type }] }))
    setTimeout(() => set(s => ({ toasts: s.toasts.filter(t => t.id !== id) })), 4000)
  },
}))

export default useUIStore