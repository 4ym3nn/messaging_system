<script setup>
import { ref, computed, watch } from 'vue'
import { chatAPI } from '../services/api'

const emit = defineEmits(['select-conversation', 'logout', 'conversation-created'])

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

const showNewConversationModal = ref(false)
const newConversationName = ref('')
const selectedUserIds = ref([])
const allUsers = ref([])
const loadingUsers = ref(false)
const memberSearchQuery = ref('')
const creatingConversation = ref(false)
const createError = ref('')

const filteredUsers = computed(() => {
  if (!memberSearchQuery.value) return allUsers.value
  return allUsers.value.filter(u =>
    u.username.toLowerCase().includes(memberSearchQuery.value.toLowerCase()) ||
    u.email.toLowerCase().includes(memberSearchQuery.value.toLowerCase())
  )
})

const canCreateConversation = computed(() => {
  return newConversationName.value.trim() !== '' && selectedUserIds.value.length > 0
})

const selectConversation = (conversation) => {
  emit('select-conversation', conversation)
}

const logout = () => {
  chatAPI.logout()
  emit('logout')
}

const fetchUsers = async () => {
  loadingUsers.value = true
  try {
    const users = await chatAPI.getUsers()
    allUsers.value = users
  } catch (error) {
    console.error('Failed to fetch users:', error)
    createError.value = 'Failed to load users'
  } finally {
    loadingUsers.value = false
  }
}

const toggleUserSelection = (userId) => {
  const index = selectedUserIds.value.indexOf(userId)
  if (index > -1) {
    selectedUserIds.value.splice(index, 1)
  } else {
    selectedUserIds.value.push(userId)
  }
}

const createNewConversation = async () => {
  if (!canCreateConversation.value) return

  creatingConversation.value = true
  createError.value = ''

  try {
    if (selectedUserIds.length<1) {
        return;
    }
    const is_group=selectedUserIds.length>1;
    const newConversation = await chatAPI.createConversation(
      newConversationName.value.trim(),
            is_group,
      selectedUserIds.value
    )
    emit('conversation-created', newConversation)
    closeNewConversationModal()
  } catch (error) {
    createError.value = error.message || 'Failed to create conversation'
  } finally {
    creatingConversation.value = false
  }
}

const closeNewConversationModal = () => {
  showNewConversationModal.value = false
  newConversationName.value = ''
  selectedUserIds.value = []
  memberSearchQuery.value = ''
  createError.value = ''
}

const openNewConversationModal = () => {
  showNewConversationModal.value = true
  if (allUsers.value.length === 0) {
    fetchUsers()
  }
}

watch(showNewConversationModal, (newVal) => {
  if (newVal && allUsers.value.length === 0) {
    fetchUsers()
  }
})
</script>

<template>
  <div class="w-80 bg-white border-r border-gray-200 flex flex-col">
    <div class="p-6 border-b border-gray-200 flex items-center justify-between">
      <h1 class="text-2xl font-bold text-gray-900">Messenger</h1>
      <div class="flex items-center gap-2">
        <button
          @click="openNewConversationModal"
          class="p-2 hover:bg-gray-100 rounded-full transition-colors"
          title="New Conversation"
        >
          <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
        </button>
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
    </div>

    <div class="p-4">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search conversations..."
        class="w-full px-4 py-2 bg-gray-100 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
      />
    </div>

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

  <!-- New Conversation Modal -->
  <div
    v-if="showNewConversationModal"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    @click.self="closeNewConversationModal"
  >
    <div class="bg-white rounded-lg w-full max-w-md p-6 m-4">
      <h2 class="text-xl font-bold text-gray-900 mb-4">New Conversation</h2>

      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-2">Conversation Name</label>
        <input
          v-model="newConversationName"
          type="text"
          placeholder="Enter conversation name"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          @keyup.enter="canCreateConversation && createNewConversation()"
        />
      </div>

      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-2">Select Members</label>
        <input
          v-model="memberSearchQuery"
          type="text"
          placeholder="Search users..."
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 mb-2"
        />
        <div class="max-h-60 overflow-y-auto border border-gray-200 rounded-lg">
          <div v-if="loadingUsers" class="p-4 text-center text-gray-500">Loading users...</div>
          <div v-else-if="filteredUsers.length === 0" class="p-4 text-center text-gray-500">No users found</div>
          <div
            v-else
            v-for="user in filteredUsers"
            :key="user.id"
            @click="toggleUserSelection(user.id)"
            class="px-4 py-3 cursor-pointer hover:bg-gray-50 flex items-center gap-3 border-b border-gray-100 last:border-b-0"
          >
            <input
              type="checkbox"
              :checked="selectedUserIds.includes(user.id)"
              class="w-4 h-4 text-indigo-600 rounded"
              @click.stop="toggleUserSelection(user.id)"
            />
            <div class="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-400 to-purple-500 flex items-center justify-center text-white font-bold flex-shrink-0">
              {{ user.username.charAt(0).toUpperCase() }}
            </div>
            <div class="flex-1 min-w-0">
              <p class="font-semibold text-gray-900 truncate">{{ user.username }}</p>
              <p class="text-sm text-gray-500 truncate">{{ user.email }}</p>
            </div>
          </div>
        </div>
      </div>

      <div v-if="selectedUserIds.length > 0" class="mb-4">
        <p class="text-sm text-gray-600">{{ selectedUserIds.length }} member(s) selected</p>
      </div>

      <div v-if="createError" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
        {{ createError }}
      </div>

      <div class="flex gap-3">
        <button
          @click="closeNewConversationModal"
          class="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
          :disabled="creatingConversation"
        >
          Cancel
        </button>
        <button
          @click="createNewConversation"
          :disabled="!canCreateConversation || creatingConversation"
          class="flex-1 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ creatingConversation ? 'Creating...' : 'Create' }}
        </button>
      </div>
    </div>
  </div>
</template>
