import { create } from 'zustand'

const useChatStore = create((set, get) => ({
  sessions: [],
  activeSessionId: null,
  messages: [],
  panelOpen: false,
  panelContent: null,
  isLoading: false,
  repoIngested: false,

  createSession: (name = 'New Chat') => {
    const id = Date.now().toString()
    const session = { id, name, createdAt: new Date() }
    set(s => ({ sessions: [session, ...s.sessions], activeSessionId: id, messages: [] }))
    return id
  },

  setActiveSession: (id) => {
    set({ activeSessionId: id, messages: [] })
  },

  addMessage: (msg) => {
    const message = { id: Date.now().toString(), timestamp: new Date(), ...msg }
    set(s => ({ messages: [...s.messages, message] }))
    return message
  },

  updateLastMessage: (patch) => {
    set(s => {
      const msgs = [...s.messages]
      msgs[msgs.length - 1] = { ...msgs[msgs.length - 1], ...patch }
      return { messages: msgs }
    })
  },

  togglePanel: (content = null) => {
    set(s => ({
      panelOpen: content ? true : !s.panelOpen,
      panelContent: content ?? s.panelContent
    }))
  },

  setLoading: (v) => set({ isLoading: v }),
  setRepoIngested: (v) => set({ repoIngested: v }),
}))

export default useChatStore