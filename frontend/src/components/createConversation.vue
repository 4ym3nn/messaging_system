<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  conversations: Array,
  selectedConversation: Object
})

const emit = defineEmits(['select', 'logout', 'conversationCreated'])

// Existing data
const searchQuery = ref('')

// New conversation modal data
const showNewConversationModal = ref(false)
const newConversationName = ref('')
const selectedUserIds = ref([])
const allUsers = ref([])
const loadingUsers = ref(false)
const memberSearchQuery = ref('')
const creatingConversation = ref(false)
const createError = ref('')

const filteredConversations = computed(() => {
  if (!searchQuery.value) return props.conversations
  return props.conversations.filter(c =>
    c.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// New computed
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

// Existing methods
const selectConversation = (conversation) => {
  emit('select', conversation)
}

const logout = () => {
  emit('logout')
}

// New methods
const fetchUsers = async () => {
  loadingUsers.value = true
  try {
    const token = localStorage.getItem('token')
    const response = await fetch('YOUR_API_BASE_URL/users', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    if (response.ok) {
      allUsers.value = await response.json()
    }
  } catch (error) {
    console.error('Failed to fetch users:', error)
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
    const token = localStorage.getItem('token')
    const response = await fetch('YOUR_API_BASE_URL/conversations', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        name: newConversationName.value.trim(),
        member_ids: selectedUserIds.value
      })
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to create conversation')
    }

    const newConversation = await response.json()
    emit('conversationCreated', newConversation)
    closeNewConversationModal()
  } catch (error) {
    createError.value = error.message
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

// Fetch users when modal opens
const openNewConversationModal = () => {
  showNewConversationModal.value = true
  if (allUsers.value.length === 0) {
    fetchUsers()
  }
}

// Watch for modal opening
const showNewConversationModalWatcher = computed(() => showNewConversationModal.value)
watch(showNewConversationModalWatcher, (newVal) => {
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
          @click="showNewConversationModal = true"
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
</template>
