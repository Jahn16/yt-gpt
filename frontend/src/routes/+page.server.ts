import type { Chat, Video } from '../models'
import { env } from '$env/dynamic/public'
import type { RequestEvent } from './$types'

export const ssr = false
export const chat: Chat = [{
  author: 'bot',
  content: "👋 I'm your YouTube Transcription Chatbot! Please share a YouTube video URL with me, and I'll extract the transcription to answer your questions based on the video's content. Just paste the URL, and let's get started!"
}]

export const load = (() => {
  return { chat }
})


let video: Video;

export const actions = {
  default: async (event) => {
    const data = await event.request.formData()
    const message = data.get('message') as string
    chat.push({ author: 'user', content: message })
    if (!video) {
      video = await getTranscription(message)
      chat.push({ author: 'bot', content: `The transcription is complete. 🎉 Please feel free to ask me any questions you have about the video's content. Let's dive in!` })
      return
    }
    const response = await callGPT(message, video)
    chat.push({ author: 'bot', content: response })
  }
}
const getTranscription = async (youtubeUrl: string): Promise<Video> => {
  const response = await fetch(`${env.PUBLIC_BACKEND_URL}/api/v1/transcribe?youtube_url=${youtubeUrl}`)
  if (!response.ok) {
    throw new Error('Failed to get transcription')
  }
  return await response.json()
}

const callGPT = async (prompt: string, video: Video): Promise<string> => {
  const data = {
    prompt: prompt,
    video: video
  }
  const response = await fetch(`${env.PUBLIC_BACKEND_URL}/api/v1/gpt`, { method: 'POST', body: JSON.stringify(data), headers: { 'Content-Type': 'application/json' } })
  return await response.json()
}

