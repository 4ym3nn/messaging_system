
<script setup>
import { ref } from 'vue'

const emit = defineEmits(['send-message'])

const messageText = ref('')

const handleSend = () => {
  if (!messageText.value.trim()) return
  emit('send-message', messageText.value)
  messageText.value = ''
}
</script>
<template>
  <div class="px-8 py-6 border-t border-gray-200">
    <div class="flex gap-3">
      <input
        v-model="messageText"
        @keyup.enter="handleSend"
        type="text"
        placeholder="Enter Message"
        class="flex-1 px-4 py-3 bg-gray-100 rounded-full focus:outline-none focus:ring-2 focus:ring-indigo-500"
      />
      <button
        @click="handleSend"
        :disabled="!messageText.trim()"
        class="px-6 py-3 bg-indigo-500 text-white rounded-full hover:bg-indigo-600 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Send
      </button>
    </div>
  </div>
</template>

