import type { Chat, shareGPTChat } from '../models';

const convertChat = (chat: Chat): shareGPTChat => {
  const items: shareGPTChat['items'] = []
  chat.forEach((chatMessage) => {
    items.push(
      {
        from: chatMessage.author === 'user' ? 'human' : 'gpt',
        value: chatMessage.content
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
