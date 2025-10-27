<script setup>
import { ref, onMounted } from 'vue'
import AuthForm from './components/AuthForm.vue'
import ContactList from './components/ContactList.vue'
import ChatWindow from './components/ChatWindow.vue'
import { chatAPI } from './services/api'

const isAuthenticated = ref(false)
const currentUser = ref(null)
const conversations = ref([])
const selectedConversation = ref(null)

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (token) {
    try {
      currentUser.value = await chatAPI.getCurrentUser()
      isAuthenticated.value = true
      await refreshConversations()
    } catch (error) {
      console.error(' Failed to load user:', error)
      localStorage.removeItem('token')
    }
  }
})

const handleAuthenticated = async () => {
  try {
    currentUser.value = await chatAPI.getCurrentUser()
    isAuthenticated.value = true
    await refreshConversations()
  } catch (error) {
    console.error(' Failed to load user:', error)
  }
}

const refreshConversations = async () => {
  try {
    conversations.value = await chatAPI.getConversations()
  } catch (error) {
    console.error(' Failed to load conversations:', error)
  }
}

const selectConversation = (conversation) => {
  selectedConversation.value = conversation
}
const handleConversationCreated = async (newConversation) => {
  try {
    await refreshConversations()
    const conversation = conversations.value.find(c => c.id === newConversation.id)
    if (conversation) {
      selectedConversation.value = conversation
    } else {
      conversations.value.push(newConversation)
      selectedConversation.value = newConversation
    }
  } catch (error) {
    console.error(' Failed to refresh conversations:', error)
    conversations.value.push(newConversation)
    selectedConversation.value = newConversation
  }
}
const handleLogout = () => {
  isAuthenticated.value = false
  currentUser.value = null
  conversations.value = []
  selectedConversation.value = null
}
</script>
<template>
  <div>
    <AuthForm v-if="!isAuthenticated" @authenticated="handleAuthenticated" />
    <div v-else class="h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex overflow-hidden">
      <div class="w-96 flex-shrink-0 border-r border-gray-200 bg-white shadow-lg">
        <ContactList
          :conversations="conversations"
          :selected-conversation="selectedConversation"
          @select-conversation="selectConversation"
          @logout="handleLogout"
        @conversation-created="handleConversationCreated"
        />
      </div>

      <div class="flex-1 flex flex-col bg-white">
        <ChatWindow
          :conversation="selectedConversation"
          :current-user-id="currentUser?.id"
          @message-sent="refreshConversations"
        />
      </div>
    </div>
  </div>
</template>
