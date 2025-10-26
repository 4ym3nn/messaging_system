
<script setup>
import { ref } from 'vue'
import { chatAPI } from '../services/api'

const emit = defineEmits(['authenticated'])

const isLogin = ref(true)
const username = ref('')
const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const handleAuth = async () => {
  error.value = ''
  loading.value = true

  try {
    if (isLogin.value) {
      await chatAPI.login(email.value, password.value)
    } else {
      await chatAPI.register(username.value, email.value, password.value)
    }
    emit('authenticated')
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>
<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-8">
    <div class="bg-white rounded-2xl shadow-2xl p-12 w-full max-w-2xl">
      <div class="text-center mb-12">
        <h1 class="text-5xl font-bold text-gray-900 mb-3">Messenger</h1>
        <p class="text-xl text-gray-600">Real-time chat application</p>
      </div>

      <div class="space-y-6">
        <!-- Username field (only for registration) -->
        <div v-if="!isLogin">
          <input
            v-model="username"
            type="text"
            placeholder="Username"
            class="w-full px-6 py-4 text-lg border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
          />
        </div>

        <!-- Email field -->
        <div>
          <input
            v-model="email"
            type="email"
            placeholder="Email"
            class="w-full px-6 py-4 text-lg border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
          />
        </div>

        <!-- Password field -->
        <div>
          <input
            v-model="password"
            type="password"
            placeholder="Password"
            class="w-full px-6 py-4 text-lg border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
          />
        </div>

        <!-- Error message -->
        <div v-if="error" class="bg-red-50 border border-red-200 text-red-600 px-6 py-4 rounded-xl text-base">
          {{ error }}
        </div>

        <!-- Submit button -->
        <button
          @click="handleAuth"
          :disabled="loading"
          class="w-full px-6 py-4 text-lg bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
        >
          {{ loading ? 'Loading...' : (isLogin ? 'Login' : 'Register') }}
        </button>

        <!-- Toggle between login/register -->
        <div class="text-center pt-4">
          <button
            @click="isLogin = !isLogin"
            class="text-indigo-600 hover:text-indigo-700 text-base font-medium transition-colors"
          >
            {{ isLogin ? 'Need an account? Register' : 'Already have an account? Login' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

