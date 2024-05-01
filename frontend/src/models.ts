export type Chat = ChatMessage[]

export interface ChatMessage {
  author: string
  content: string
}

export interface Video {
  title: string
  transcription: string
}
