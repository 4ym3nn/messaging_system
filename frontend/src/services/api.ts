const API_BASE_URL = "http://localhost:8000/api"

export interface User {
  id: string
  username: string
  email: string
}

export interface Message {
  id: string
  conversation_id: string
  sender_id: string
  content: string
  created_at: string
}

export interface Conversation {
  id: string
  name: string
  members: User[]
  last_message?: Message
  created_at: string
}

class ChatAPI {
  private token: string | null = localStorage.getItem("token")

  private getHeaders() {
        return {
      "Content-Type": "application/json",
      ...(this.token && { Authorization: `Bearer ${this.token}` }),
    }
  }

  async register(username: string, email: string, password: string) {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: "POST",
      headers: this.getHeaders(),
      body: JSON.stringify({ username, email, password }),
    })
    if (!response.ok) throw new Error("Registration failed")
    const data = await response.json()
    this.token = data.access_token
    localStorage.setItem("token", data.access_token)
    localStorage.setItem("user_id",data.user_id);
    return data
  }

  async login(email: string, password: string) {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: "POST",
      headers: this.getHeaders(),
      body: JSON.stringify({ email, password }),
    })
    if (!response.ok) throw new Error("Login failed")
    const data = await response.json()
    this.token = data.access_token
    localStorage.setItem("token", data.access_token)
    localStorage.setItem("user_id",data.user_id);
    return data
  }

  logout() {
    this.token = null
    localStorage.removeItem("token")
  }

  async getCurrentUser(): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/users/me`, {
      headers: this.getHeaders(),
    })
    if (!response.ok) throw new Error("Failed to fetch user")
    return response.json()
  }

  async getConversations(): Promise<Conversation[]> {
    const response = await fetch(`${API_BASE_URL}/conversations`, {
      headers: this.getHeaders(),
    })
    if (!response.ok) throw new Error("Failed to fetch conversations")
    return response.json()
  }

  async getConversation(conversationId: string): Promise<Conversation> {
    const response = await fetch(`${API_BASE_URL}/conversations/${conversationId}`, {
      headers: this.getHeaders(),
    })
    if (!response.ok) throw new Error("Failed to fetch conversation")
    return response.json()
  }

  async createConversation(name: string,is_group=true, memberIds: string[]): Promise<Conversation> {
    const response = await fetch(`${API_BASE_URL}/conversations`, {
      method: "POST",
      headers: this.getHeaders(),
      body: JSON.stringify({ name,is_group, member_ids: memberIds }),
    })
    if (!response.ok) throw new Error("Failed to create conversation")
    return response.json()
  }

  async getMessages(conversationId: string): Promise<Message[]> {
    const response = await fetch(`${API_BASE_URL}/conversations/${conversationId}/messages`, {
      headers: this.getHeaders(),
    })
    if (!response.ok) throw new Error("Failed to fetch messages")
    return response.json()
  }
  async getUsers(): Promise<User[]> {
    const response = await fetch(`${API_BASE_URL}/users/`, {
      headers: this.getHeaders(),
    })
    if (!response.ok) throw new Error("Failed to fetch messages")
    return response.json()
  }


  async sendMessage(conversationId: string, content: string): Promise<Message> {
    const response = await fetch(`${API_BASE_URL}/conversations/${conversationId}/messages`, {
      method: "POST",
      headers: this.getHeaders(),
      body: JSON.stringify({ content }),
    })
    if (!response.ok) throw new Error("Failed to send message")
    return response.json()
  }

  connectWebSocket(conversationId: string, onMessage: (message: Message) => void) {
    const userId = localStorage.getItem('user_id');
    const wsUrl = `ws://localhost:8000/ws/${conversationId}/${userId}?token=${this.token}`
    const ws = new WebSocket(wsUrl)

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data)
      onMessage(message)
    }

    ws.onerror = (error) => {
      console.error(" WebSocket error:", error)
    }

    return ws
  }
}

export const chatAPI = new ChatAPI()
