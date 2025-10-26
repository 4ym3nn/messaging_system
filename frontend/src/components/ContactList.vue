<script setup>
import { ref, computed } from 'vue'
import { chatAPI } from '../services/api'

const emit = defineEmits(['select-conversation', 'logout'])

const props = defineProps({
  conversations: Array,
  selectedConversation: Object
})

const searchQuery = ref('')

const filteredConversations = computed(() => {
  if (!searchQuery.value) return props.conversations || []
  return (props.conversations || []).filter(conv =>
    conv.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const selectConversation = (conversation) => {
  emit('select-conversation', conversation)
}

const logout = () => {
  chatAPI.logout()
  emit('logout')
}
</script>
<template>
  <div class="w-80 bg-white border-r border-gray-200 flex flex-col">
    <!-- Header -->
    <div class="p-6 border-b border-gray-200 flex items-center justify-between">
      <h1 class="text-2xl font-bold text-gray-900">Messenger</h1>
      <button
        @click="logout"
        class="p-2 hover:bg-gray-100 rounded-full transition-colors"
        title="Logout"
      >
        <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
        </svg>
      </button>
    </div>

    <!-- Search -->
    <div class="p-4">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search conversations..."
        class="w-full px-4 py-2 bg-gray-100 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
      />
    </div>

    <!-- Contacts List -->
    <div class="flex-1 overflow-y-auto">
      <div v-if="filteredConversations.length === 0" class="p-4 text-center text-gray-500">
        No conversations yet
      </div>
      <div
        v-for="conversation in filteredConversations"
        :key="conversation.id"
        @click="selectConversation(conversation)"
        :class="[
          'px-4 py-3 cursor-pointer border-l-4 transition-colors',
          selectedConversation?.id === conversation.id
            ? 'bg-indigo-50 border-indigo-500'
            : 'border-transparent hover:bg-gray-50'
        ]"
      >
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 rounded-full bg-gradient-to-br from-indigo-400 to-purple-500 flex items-center justify-center text-white font-bold flex-shrink-0">
            {{ conversation.name.charAt(0) }}
          </div>
          <div class="flex-1 min-w-0">
            <p class="font-semibold text-gray-900 truncate">{{ conversation.name }}</p>
            <p class="text-sm text-gray-500 truncate">{{ conversation.last_message?.content || 'No messages yet' }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


