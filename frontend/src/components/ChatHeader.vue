<template>
  <div v-if="conversation" class="px-8 py-6 border-b border-gray-200 flex items-center justify-between">
    <div class="flex items-center gap-4">
      <div class="w-12 h-12 rounded-full bg-gradient-to-br from-indigo-400 to-purple-500 flex items-center justify-center text-white font-bold">
        {{ conversation.name.charAt(0) }}
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900">{{ conversation.name }}</h2>
        <p class="text-sm text-gray-500">{{ conversation.members?.length || 0 }} members</p>
      </div>
    </div>
    <div class="flex gap-4">
      <button class="p-2 hover:bg-gray-100 rounded-full transition-colors">
        <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
        </svg>
      </button>
      <button class="p-2 hover:bg-gray-100 rounded-full transition-colors">
        <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  conversation: Object
})
</script>
