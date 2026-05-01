import React, { useEffect, useRef } from 'react'
import useChatStore from '../../store/useChatStore'
import { MessageBubble } from './messageBubble'
import { WelcomeState } from './WelcomeState'

export function MessageList() {
  const messages = useChatStore(s => s.messages)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  return (
    <div style={{ flex: 1, overflowY: 'auto', padding: '24px 20px' }}>
      {messages.length === 0
        ? <WelcomeState />
        : messages.map(msg => <MessageBubble key={msg.id} msg={msg} />)
      }
      <div ref={bottomRef} />
    </div>
  )
}