import React from 'react'
import { UserMessage } from './UserMessage'
import { BotMessage } from './BotMessage'

export function MessageBubble({ msg }) {
  return msg.role === 'user'
    ? <UserMessage content={msg.content} />
    : <BotMessage content={msg.content} loading={msg.loading} error={msg.error} />
}