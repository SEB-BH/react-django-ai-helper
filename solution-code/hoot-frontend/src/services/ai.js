const BASE_URL = `${import.meta.env.VITE_BACK_END_SERVER_URL}/ai/ask`

const sendMessage = async (messages) => {
  const response = await fetch(BASE_URL, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${localStorage.getItem('token')}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ messages }),
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.err || 'The AI assistant could not answer.')
  }

  return data
}

export {
  sendMessage,
}
