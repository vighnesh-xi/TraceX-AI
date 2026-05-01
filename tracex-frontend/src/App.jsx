import React from 'react'
import { Sidebar } from './components/layout/Sidebar'
import { Topbar } from './components/layout/Topbar'
import { RightPanel } from './components/layout/RightPanel'
import { MessageList } from './components/chat/MessageList'
import { QueryComposer } from './components/input/QueryComposer'
import { IngestModal } from './components/modals/IngestModal'
import { ToastContainer } from './components/ui/Toast'
import { useTheme } from './hooks/useTheme'
import useChatStore from './store/useChatStore'

export default function App() {
  useTheme()
  const panelOpen = useChatStore(s => s.panelOpen)

  return (
    <>
      <div style={{ display: 'flex', height: '100dvh', overflow: 'hidden' }}>
        <Sidebar />
        <main style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden', minWidth: 0 }}>
          <Topbar />
          <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
            <section style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden', minWidth: 0 }}>
              <MessageList />
              <QueryComposer />
            </section>
            {panelOpen && <RightPanel />}
          </div>
        </main>
      </div>
      <IngestModal />
      <ToastContainer />
    </>
  )
}