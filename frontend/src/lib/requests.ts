// place files you want to import through the `$lib` alias in this folder.
import { env } from '$env/dynamic/public';
import type { Video } from '../models'


export const getTranscription = async (youtubeUrl: string): Promise<Video> => {
  const response = await fetch(`${env.PUBLIC_BACKEND_URL}/api/v1/transcribe?youtube_url=${youtubeUrl}`)
  if (!response.ok) {
    throw new Error('Failed to get transcription')
  }
  return await response.json()
}

export const callGPT = async (prompt: string, video: Video): Promise<string> => {
  const data = {
    prompt: prompt,
    video: video
  }
  const response = await fetch(`${env.PUBLIC_BACKEND_URL}/api/v1/gpt`, { method: 'POST', body: JSON.stringify(data), headers: { 'Content-Type': 'application/json' } })
  return await response.json()
}
