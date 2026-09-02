import { useState } from 'react'

import * as aiService from '../services/ai'

const AIHelper = () => {
  const [messages, setMessages] = useState([])
  const [formData, setFormData] = useState('')
  const [isSending, setIsSending] = useState(false)
  const [errorMessage, setErrorMessage] = useState('')

  const handleChange = (event) => {
    setFormData(event.target.value)
  }

  const handleSubmit = async (event) => {
    event.preventDefault()

    const trimmedMessage = formData.trim()

    if (!trimmedMessage || isSending) {
      return
    }

    const userMessage = {
      role: 'user',
      text: trimmedMessage,
    }

    const nextMessages = [...messages, userMessage]

    setMessages(nextMessages)
    setFormData('')
    setErrorMessage('')
    setIsSending(true)

    try {
      const data = await aiService.sendMessage(nextMessages)

      const assistantMessage = {
        role: 'assistant',
        text: data.reply,
      }

      setMessages([...nextMessages, assistantMessage])
    } catch (error) {
      setMessages(messages)
      setFormData(trimmedMessage)
      setErrorMessage(error.message)
    } finally {
      setIsSending(false)
    }
  }

  const handleClear = () => {
    setMessages([])
    setFormData('')
    setErrorMessage('')
  }

  return (
    <section className="card ai-helper">
      <header>
        <h1>Hoot AI Helper</h1>
        <p>Ask a question and continue the conversation.</p>
      </header>

      <section
        className="ai-helper-messages"
        aria-live="polite"
        aria-busy={isSending}
      >
        {messages.length === 0 && (
          <p className="ai-helper-empty">
            No messages yet. Ask Hoot Helper a question.
          </p>
        )}

        {messages.map((message, index) => (
          <article
            className={`ai-message ai-message-${message.role}`}
            key={`${message.role}-${index}`}
          >
            <strong>
              {message.role === 'user' ? 'You' : 'Hoot Helper'}
            </strong>
            <p>{message.text}</p>
          </article>
        ))}

        {isSending && (
          <p className="ai-helper-status">Hoot Helper is thinking...</p>
        )}
      </section>

      {errorMessage && (
        <p className="ai-helper-error" role="alert">
          {errorMessage}
        </p>
      )}

      <form onSubmit={handleSubmit}>
        <label htmlFor="message">Message</label>
        <textarea
          id="message"
          name="message"
          rows="3"
          maxLength="2000"
          value={formData}
          onChange={handleChange}
          placeholder="Ask Hoot Helper..."
        />

        <div className="ai-helper-actions">
          <button
            type="submit"
            disabled={!formData.trim() || isSending}
          >
            {isSending ? 'SENDING...' : 'SEND'}
          </button>
          <button
            className="secondary-button"
            type="button"
            disabled={
              isSending || (messages.length === 0 && !errorMessage)
            }
            onClick={handleClear}
          >
            CLEAR CONVERSATION
          </button>
        </div>
      </form>

      <p className="ai-helper-note">
        Use test content only. Do not share passwords, personal information,
        or private client data with the AI service.
      </p>
    </section>
  )
}

export default AIHelper
