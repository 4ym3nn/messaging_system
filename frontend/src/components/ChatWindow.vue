<script setup>
import { ref, watch, nextTick } from 'vue'
import ChatHeader from './ChatHeader.vue'
import MessageInput from './MessageInput.vue'
import { chatAPI } from '../services/api'

const props = defineProps({
  conversation: Object,
  currentUserId: String
})

const emit = defineEmits(['message-sent'])

const messages = ref([])
const messagesContainer = ref(null)
let ws = null

watch(() => props.conversation?.id, async (newConvId) => {
  if (!newConvId) return

  // Close previous WebSocket connection
  if (ws) ws.close()

  // Fetch messages
  try {
    messages.value = await chatAPI.getMessages(newConvId)
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('[v0] Failed to fetch messages:', error)
  }

  ws = chatAPI.connectWebSocket(newConvId, (message) => {
    messages.value.push(message)
    nextTick(() => scrollToBottom())
  })
})

const sendMessage = async (content) => {
  if (!props.conversation) return

  try {
    const message = await chatAPI.sendMessage(props.conversation.id, content)
    messages.value.push(message)
    await nextTick()
    scrollToBottom()
    emit('message-sent')
  } catch (error) {
    console.error('[v0] Failed to send message:', error)
  }
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const formatTime = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
}
</script>
<template>
  <div class="flex-1 flex flex-col bg-white">
    <ChatHeader :conversation="conversation" />

    <!-- Messages -->
    <div v-if="conversation" class="flex-1 overflow-y-auto p-8 space-y-4" ref="messagesContainer">
      <div
        v-for="message in messages"
        :key="message.id"
        :class="[
          'flex gap-3',
          message.sender_id === currentUserId ? 'justify-end' : 'justify-start'
        ]"
      >
        <div v-if="message.sender_id !== currentUserId" class="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-400 to-purple-500 flex-shrink-0"></div>
        <div
          :class="[
            'max-w-xs px-4 py-2 rounded-lg',
            message.sender_id === currentUserId
              ? 'bg-indigo-500 text-white rounded-br-none'
              : 'bg-gray-100 text-gray-900 rounded-bl-none'
          ]"
        >
          <p class="text-sm">{{ message.content }}</p>
          <p :class="['text-xs mt-1', message.sender_id === currentUserId ? 'text-indigo-100' : 'text-gray-500']">
            {{ formatTime(message.created_at) }}
          </p>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="flex-1 flex items-center justify-center">
      <div class="text-center">
        <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>
        <p class="text-gray-500 text-lg">Select a conversation to start messaging</p>
      </div>
    </div>

    <!-- Message Input -->
    <MessageInput v-if="conversation" @send-message="sendMessage" />
  </div>
</template>


