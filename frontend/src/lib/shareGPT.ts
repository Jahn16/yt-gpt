import type { Chat, shareGPTChat } from '../models';
import { marked } from 'marked';

const markdownToHTML = (markdown: string): string => {
  let render = new marked.Renderer();
  render.paragraph = (text) => {
    return text
  }
  render.link = (href, title, text) => {
    return text
  }
  return marked(markdown, { renderer: render })
}

const convertChat = (chat: Chat): shareGPTChat => {
  const items: shareGPTChat['items'] = []
  chat.forEach((chatMessage) => {
    items.push(
      {
        from: chatMessage.author === 'user' ? 'human' : 'gpt',
        value: markdownToHTML(chatMessage.content)
      }
    )
  })
  return {
    avatarUrl: '',
    items: items
  }


}
export const submitChat = async (chat: Chat) => {
  const convertedChat = convertChat(chat)
  console.log(convertedChat)
  const request = await fetch('https://sharegpt.com/api/conversations', {
    method: 'POST',
    body: JSON.stringify(convertedChat),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  const response = await request.json()
  if (!request.ok) {
    console.log(response)
  }
  const { id } = response
  const url = `https://shareg.pt/${id}`
  window.open(url, '_blank')
}
