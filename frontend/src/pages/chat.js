import React from 'react'
import ChatBox from '../components/ChatBox'

export default function ChatPage() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Assistant IA</h1>
      <ChatBox apiUrl="/qa" />
    </div>
  )
}
